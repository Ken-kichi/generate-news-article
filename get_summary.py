

def main():
    with open("output/20260417_090640_edited_ver1.md", "r") as f:
        content = f.read()
        split_content = content.split("\n\n")
        summary = split_content[0] + "\n" + split_content[4]
        print(summary)


if __name__ == "__main__":
    main()
