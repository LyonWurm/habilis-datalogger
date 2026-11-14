# hook.py
from pathlib import Path
from pythonforandroid.toolchain import ToolchainCL, info

def after_apk_build(toolchain: ToolchainCL):
    """Patch manifest and stage resource right before APK packaging."""
    dist_dir = Path(toolchain._dist.dist_dir) / "src" / "main"
    
    # 1. Stage filepaths.xml
    src_xml = Path(__file__).parent / "android" / "res" / "xml" / "filepaths.xml"
    dst_xml_dir = dist_dir / "res" / "xml"
    dst_xml_dir.mkdir(parents=True, exist_ok=True)
    if src_xml.exists():
        import shutil
        shutil.copy(src_xml, dst_xml_dir / "filepaths.xml")
        info(f"[hook] Staged filepaths.xml at {dst_xml_dir}")
    
    # 2. Patch manifest
    manifest = dist_dir / "AndroidManifest.xml"
    if not manifest.exists():
        info(f"[hook] Manifest missing at {manifest}")
        return
    
    content = manifest.read_text()
    if "fileprovider" in content:
        info("[hook] Manifest already patched")
        return
    
    provider = """
        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="org.kffs.habilisdatalogger.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/filepaths" />
        </provider>
"""
    content = content.replace("</application>", provider + "    </application>", 1)
    manifest.write_text(content)
    info("[hook] Patched manifest with provider")
