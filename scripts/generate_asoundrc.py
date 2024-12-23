import os
import subprocess


def check_asoundrc_exists():
    home_dir = os.path.expanduser("~")
    asoundrc_path = os.path.join(home_dir, ".asoundrc")
    return os.path.exists(asoundrc_path)


def get_default_audio_device():
    result = subprocess.run(['aplay', '-l'], capture_output=True, text=True)
    output = result.stdout

    for line in output.splitlines():
        if "card" in line:
            parts = line.split(',')
            card_info = parts[0].strip().split()
            card = card_info[1].rstrip(':')
            device_info = parts[1].strip().split()
            device = device_info[1].rstrip(':')

            return int(card), int(device)

    raise RuntimeError("No audio device found")


def generate_asoundrc_content(card, device):
    return (
        f"defaults.pcm.card {card}\r\n"
        f"defaults.pcm.device {device}\r\n"
        f"defaults.ctl.card {card}\r\n"
    )


def write_asoundrc(content):
    home_dir = os.path.expanduser("~")
    asoundrc_path = os.path.join(home_dir, ".asoundrc")
    with open(asoundrc_path, "w") as file:
        file.write(content)
    print(f"Generated {asoundrc_path}")


def main():
    if check_asoundrc_exists():
        print("~/.asoundrc already exists. No changes made.")
        return

    try:
        card, device = get_default_audio_device()
        asoundrc_content = generate_asoundrc_content(card, device)
        write_asoundrc(asoundrc_content)
    except RuntimeError as e:
        print(e)


if __name__ == "__main__":
    main()
