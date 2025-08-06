# IPGrinder

**IPGrinder** is a DDoS script intended for **stress testing infrastructure**.

> ⚠️ This tool is meant for **educational and ethical testing purposes only**. Do **not** use it on networks or systems without explicit authorization.

---

## 🔧 Setup for Fakeroot

### Manual Steps

```bash
apt-get update && apt-get upgrade -y
apt-get install git -y
git clone https://github.com/adarshaddee/root.git
cd root
chmod +x main
./main
```

### One-liner

```bash
pkg --check-mirror update && apt-get update && apt-get upgrade -y && apt-get install git -y && git clone https://github.com/adarshaddee/root.git && cd root && chmod +x main && ./main
```

---

## ⚙️ Setup for IPGrinder

### Manual Steps

```bash
pkg update && pkg upgrade -y
pkg install git python -y
git clone https://github.com/NeoMatrix14241/IPGrinder.git
cd IPGrinder
python ipgrinder.py
```

### One-liner

```bash
pkg --check-mirror update && pkg update && pkg upgrade -y && pkg install git python -y && git clone https://github.com/NeoMatrix14241/IPGrinder.git && cd IPGrinder && python ipgrinder.py
```

---

## 🚀 Usage

```bash
python ipgrinder.py <IP> <PORT> [PROTOCOLS] [THREADS_PER_PROTO] [PACKET_SIZE]
```

### Parameters

- `<IP>` – Target IP address
- `<PORT>` – Target port
- `[PROTOCOLS]` – Comma-separated list of protocols (udp, tcp, icmp, http, all)
- `[THREADS_PER_PROTO]` – Number of threads per selected protocol
- `[PACKET_SIZE]` – Size of each packet in bytes

### Example

```bash
python ipgrinder.py 192.168.1.1 80 tcp,udp 100 1024
```

---

**Disclaimer:** The creator is **not responsible** for any misuse or damage caused by this tool.
