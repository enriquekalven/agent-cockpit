import os
import shutil


def sync_docs():
    """
    Synchronizes core documentation files from root and /docs to /public.
    Ensures the website reflects the latest Master Architect standards.
    """
    sync_map = {
        "ROADMAP.md": "public/ROADMAP.md",
        "CHANGELOG.md": "public/CHANGELOG.md",
        "README.md": "public/README.md",
        "docs/PRD.md": "public/PRD.md",
        "docs/ROADMAP_V13.md": "public/ROADMAP_V13.md",
        "docs/TECHNICAL_UX_GUIDE.md": "public/TECHNICAL_UX_GUIDE.md",
        "docs/TECHNICAL_AUDIT_GUIDE.md": "public/TECHNICAL_AUDIT_GUIDE.md",
        "docs/TECHNICAL_FINOPS_GUIDE.md": "public/TECHNICAL_FINOPS_GUIDE.md",
        "docs/TECHNICAL_INFRA_GUIDE.md": "public/TECHNICAL_INFRA_GUIDE.md",
        "docs/TECHNICAL_QUALITY_GUIDE.md": "public/TECHNICAL_QUALITY_GUIDE.md",
        "docs/TECHNICAL_REDTEAM_GUIDE.md": "public/TECHNICAL_REDTEAM_GUIDE.md",
    }

    print("🛰️ Documentation Sync Initialized...")
    for src, dst in sync_map.items():
        if os.path.exists(src):
            # Special handling for some files if needed (e.g. command search/replace)
            # For now, we do high-fidelity direct sync as requested.
            shutil.copy2(src, dst)
            print(f"✅ Synced: {src} -> {dst}")
        else:
            print(f"⚠️ Source not found: {src}")

if __name__ == "__main__":
    sync_docs()
