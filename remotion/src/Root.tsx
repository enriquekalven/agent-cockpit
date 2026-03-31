import { Composition } from 'remotion';
import { EvolveDemo } from './EvolveDemo';
import { StandaloneUpgradeDemo } from './EvolveDemo/StandaloneUpgradeDemo';
import { StandaloneMCPDemo } from './EvolveDemo/StandaloneMCPDemo';
import { StandaloneCertifyDemo } from './EvolveDemo/StandaloneCertifyDemo';
import { StandaloneLadderDemo } from './EvolveDemo/StandaloneLadderDemo';
import { StandaloneExplainerDemo } from './EvolveDemo/StandaloneExplainerDemo';
import { AgentOpsCockpitDemo } from './EvolveDemo/AgentOpsCockpitDemo';
import { StandaloneEvolveDeepDiveDemo } from './EvolveDemo/StandaloneEvolveDeepDiveDemo';
import { StandaloneGettingStartedDemo } from './GettingStartedDemo/StandaloneGettingStartedDemo';
import { StandaloneEvolveStoryDemo } from './EvolveDemo/StandaloneEvolveStoryDemo';
import { StandaloneCertifyStoryDemo } from './EvolveDemo/StandaloneCertifyStoryDemo';
import { StandaloneUpgradeStoryDemo } from './EvolveDemo/StandaloneUpgradeStoryDemo';

export const RemotionRoot = () => {
  return (
    <>
      <Composition
        id="EvolveDemo"
        component={EvolveDemo}
        durationInFrames={1185}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="UpgradeDemo-ADK-Overhaul"
        component={StandaloneUpgradeDemo}
        durationInFrames={520}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="MCPDemo-ADK-Handshake"
        component={StandaloneMCPDemo}
        durationInFrames={540}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="CertifyDemo-Governance-Seal"
        component={StandaloneCertifyDemo}
        durationInFrames={520}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="AgentOpsCockpit-FullDemo"
        component={AgentOpsCockpitDemo}
        durationInFrames={1415}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="LadderDemo-Autonomy-Scale"
        component={StandaloneLadderDemo}
        durationInFrames={2700}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="ExplainerDemo-Executive-Summary"
        component={StandaloneExplainerDemo}
        durationInFrames={690}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="EvolveDeepDive-Technical-Analysis"
        component={StandaloneEvolveDeepDiveDemo}
        durationInFrames={1590}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="GettingStarted-Walkthrough"
        component={StandaloneGettingStartedDemo}
        durationInFrames={790}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="Evolve-The-Story"
        component={StandaloneEvolveStoryDemo}
        durationInFrames={1175}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="Certify-The-Story"
        component={StandaloneCertifyStoryDemo}
        durationInFrames={1175}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="Upgrade-The-Story"
        component={StandaloneUpgradeStoryDemo}
        durationInFrames={1175}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
