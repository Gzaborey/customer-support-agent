from app.common.utils import update_faq


def main() -> None:
    """
    Script to create a new update FAQ file form existing .txt FAQ file and existing .txt customizations file.
    """
    update_faq(r"data\processed\faq_doc.txt",
               r"data\processed\customizations_doc.txt",
               r"data\processed\updated_faq_doc.txt")


if __name__=="__main__":
    main()