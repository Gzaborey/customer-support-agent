from common.utils import update_faq


def main() -> None:
    update_faq(r"data\processed\faq_doc.txt",
               r"data\processed\customizations_doc.txt",
               r"data\processed\updated_faq_doc.txt")


if __name__=="__main__":
    main()