import unicodedata
import click

abeceda = "abcdefghijklmnopqrstuvwxyz"

def caesarovasifra(text, posun, vystup):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").lower()
    sifra = ""
    for char in text:
        if char not in abeceda:
            sifra += char
        else:
            sifra += abeceda[(abeceda.index(char) + posun) % len(abeceda)]

    if vystup:
        with open(vystup, "w") as file:
            file.write(sifra)
    else:
        print(sifra)

@click.command()
@click.option("-p", "--posun", default=3, help="Posun při šifrování/dešifrování")
@click.argument("text", required=False)
@click.option("-v", "--vystup", default="", help="Místo uložení")

def main(text, posun, vystup):
    if not text:
        text = input("Zadejte text k šifrování/dešifrování: ")
    caesarovasifra(text, posun, vystup)

if __name__ == '__main__':
    main()