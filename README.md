# IPGrinder

**IPGrinder** is a multi-threaded DDoS script intended for **stress testing infrastructure**.

> ⚠️ This tool is meant for **educational and ethical testing purposes only**. Do **not** use it on networks or systems without explicit authorization.

---

## ⚙️ Setup Instructions

### 📱 Termux (Android)

> 🛑 These commands are for **Termux only**. Do not run them on regular Linux distros.

#### 🔧 Manual Steps

```bash
pkg --check-mirror update
pkg update && pkg upgrade -y
pkg install git python -y
git clone https://github.com/NeoMatrix14241/IPGrinder.git
cd IPGrinder
python -m pip install requests
python ipgrinder.py
```

#### ⚡ One-liner

```bash
pkg --check-mirror update && pkg update && pkg upgrade -y && pkg install git python -y && git clone https://github.com/NeoMatrix14241/IPGrinder.git && cd IPGrinder && python -m pip install requests && python ipgrinder.py
```

---

### 🖥️ Linux (Debian/Ubuntu)

> ✅ Works on most Debian-based distros. Adjust `apt` to your package manager if you're using Arch, Fedora, etc.

#### 🔧 Manual Steps

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git python3 python3-pip -y
git clone https://github.com/NeoMatrix14241/IPGrinder.git
cd IPGrinder
python3 -m pip install --upgrade pip
python3 -m pip install requests
python3 ipgrinder.py
```

#### ⚡ One-liner

```bash
sudo apt update && sudo apt upgrade -y && sudo apt install git python3 python3-pip -y && git clone https://github.com/NeoMatrix14241/IPGrinder.git && cd IPGrinder && python3 -m pip install --upgrade pip && python3 -m pip install requests && python3 ipgrinder.py
```

---

## 🚀 Usage

```bash
python ipgrinder.py <IP> <PORT> [PROTOCOLS] [THREADS_PER_PROTO] [PACKET_SIZE]
```

---

## ⚠️ ICMP Protocol Usage on Termux

> 🛑 **Important:** ICMP (e.g., ping-based attacks) requires **root access** on Android.
>
> - Your device must be **rooted**.
> - You must have a working `su` binary (e.g., installed via **Magisk**).
> - Without root, `icmp` will fail due to raw socket restrictions.
>
> Other protocols like `udp`, `tcp`, and `http` **do not require root** and will work in non-rooted Termux.


### Parameters

- `<IP>` – Target IP address
- `<PORT>` – Target port
- `[PROTOCOLS]` – Comma-separated list of protocols (udp, tcp, icmp, http, all)
- `[THREADS_PER_PROTO]` – Number of threads per selected protocol
- `[PACKET_SIZE]` – Size of each packet in bytes

### 💡 Example

```bash
python ipgrinder.py 192.168.1.1 80 tcp,udp 100 1024 # <-- For TCP/UDP
python ipgrinder.py 192.168.1.1 80 icmp 100 1024 # <-- For ICMP
python ipgrinder.py 192.168.1.1 80 tcp,udp,http 100 1024 # <-- For TCP/UDP/HTTP
python ipgrinder.py 192.168.1.1 80 all 100 1024 # <-- For all protocols supported (TCP,UDP,HTTP,ICMP)
```

---

## ⚠️ Disclaimer

The creator is **not responsible** for any misuse, damage, or legal consequences resulting from the use of this tool. Use it **only on infrastructure you own or have explicit permission to test**.
