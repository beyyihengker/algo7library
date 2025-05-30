import os

def clear_screen():
    """Membersihkan layar terminal."""
    os.system("cls" if os.name == "nt" else "clear")

def header(*title):
    """Sebagai header aplikasi."""
    clear_screen()
    print("============˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊============")
    for i in title:
        placeholder = " " * (len(i) + 4)
        fill = "═" * (15 - (len(i)//2))
        print(f"{fill} {i.center(len(placeholder))} {fill}")
    print("============˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊============")

def footer():
    """Sebagai footer aplikasi."""
    print("===========  TERIMA KASIH  ==========")
    print("=========  TELAH BERKUNJUNG  ========")
    print("============˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊============")
