import React from 'react';
import { AbsoluteFill, staticFile } from 'remotion';
import { Audio } from '@remotion/media';
import { EvolveDeepDiveScene } from './EvolveDeepDiveScene';
import { EvolveSampleScene } from './EvolveSampleScene';
import { TitleScene } from './TitleScene';
import { ClosingScene } from './ClosingScene';
import { TransitionSeries, linearTiming } from '@remotion/transitions';
import { fade } from '@remotion/transitions/fade';

export const StandaloneEvolveDeepDiveDemo: React.FC = () => {

  const sampleArch = {
    pillarName: "Architecture",
    filename: "agent.py",
    problem: "A massive monolithic script acting as a 'Spaghetti Agent'. Hard to test or scale.",
    command: "uvx agentops-cockpit evolve",
    benefits: "Modular routers injected; passive patterns converted to managed RAG.",
    summary: "Architecture decoupled and hardened for production scale.",
    legacyCode: `def main():
    while True:
        prompt = input("User: ")
        # MASSIVE MONOLITH
        if "weather" in prompt:
            get_weather()
        elif "docs" in prompt:
            passive_retrieval()`,
    newCode: `@app.command()
async def main():
    router = ModularRouter(
        intents=["weather", "search"]
    )
    
    # Decider Logic Injected
    intent = await router.route(prompt)
    if intent == 'RAG':
         await run_managed_rag(prompt)`
  };

  const sampleReliability = {
    pillarName: "Reliability",
    filename: "sales_agent.py",
    problem: "Naked tool calls risking zombie agents and hanging LLM execution states.",
    command: "uvx agentops-cockpit evolve",
    benefits: "Exponential backoff, timeout protection, and telemetry tracing injected.",
    summary: "Poka-Yoke resiliency natively baked in.",
    legacyCode: `def execute_tool(func, args):
    # Fragile Tool Invocation
    # No timeouts, no retries, hanging risk
    return func(**args)

def query_database():
    results = db.query("SELECT *")
    return results`,
    newCode: `# Poka-Yoke + Resiliency injected
@retry(wait=exponential(min=1, max=10), stop=3)
@telemetry.trace("tool_execution")
def execute_tool(func, args):
    with timeout(30): # Zombie protection
        return func(**args)

@telemetry.trace("db_query")
def query_database(): ...`
  };

  const sampleFinops = {
    pillarName: "FinOps",
    filename: "payloads.py",
    problem: "Hemorrhaging tokens by continuously sending massive static system prompts.",
    command: "uvx agentops-cockpit evolve",
    benefits: "Gemini Context-Caching automatically applied to static payload execution.",
    summary: "Projected OPEX reduced by 90% via context optimization.",
    legacyCode: `def generate_response(docs):
    # Sends millions of tokens every turn
    model = GenerativeModel("gemini-1.5-pro")
    
    return model.generate_content([
        sys_prompt, 
        *docs, 
        user_query
    ])`,
    newCode: `def generate_response(docs):
    # Context Caching applied autonomously
    cache = ContextCacheManager.create(
        model="gemini-1.5-pro",
        contents=[sys_prompt, *docs]
    )
    model = GenerativeModel("gemini-1.5-pro")
    
    return model.generate_content(
        user_query, 
        opt=cache.config() # 90% Cost Reduction
    )`
  };

  const sampleSecurity = {
    pillarName: "Security",
    filename: "ops_bot.py",
    problem: "Insecure tool execution vulnerable to lateral movement and prompt injection.",
    command: "uvx agentops-cockpit evolve",
    benefits: "Declarative Guardrails and Privilege Check gates structurally isolated.",
    summary: "Secured capabilities restricted by strict user scope.",
    legacyCode: `class OpsAgent:
    def __init__(self):
        self.tools = [bash_executor, db_nuke]
        
    def run_command(self, cmd):
        # Insecure Execution
        return bash_executor(cmd)`,
    newCode: `class OpsAgent:
    def __init__(self):
        self.tools = [Secured(bash_executor)]
        
    @tool_privilege_check(scope="admin")
    def run_command(self, cmd):
        # Scaffolded policy engine guards
        # Prevents lateral movement
        return bash_executor(cmd)`
  };

  return (
    <AbsoluteFill style={{ background: '#0a0a1a' }}>
      <Audio src={staticFile('bgm-corporate.mp3')} volume={0.3} />
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={120}>
          <TitleScene title="Evolve Deep Dive" command="uvx agentops-cockpit evolve" />
        </TransitionSeries.Sequence>
        
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />
        <TransitionSeries.Sequence durationInFrames={450}>
          <EvolveDeepDiveScene />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />
        <TransitionSeries.Sequence durationInFrames={240}>
          <EvolveSampleScene {...sampleArch} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />
        <TransitionSeries.Sequence durationInFrames={240}>
          <EvolveSampleScene {...sampleReliability} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />
        <TransitionSeries.Sequence durationInFrames={240}>
          <EvolveSampleScene {...sampleFinops} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />
        <TransitionSeries.Sequence durationInFrames={240}>
          <EvolveSampleScene {...sampleSecurity} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />
        <TransitionSeries.Sequence durationInFrames={150}>
          <ClosingScene />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};
