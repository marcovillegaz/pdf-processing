""""https://github.com/DaDataGuy/PDF_Merged_Script/blob/main/Python_Script/PDF%20Python%20Merge%20Script.ipynb"""

import os
import PyPDF2


def gen_identify(family):
    # This function identify the parent and the childs
    for individual in family:
        if isinstance(individual, dict):
            parent = individual

        elif isinstance(individual, list):
            childs = individual

    return parent, childs


def bookmarks_family_tree(outlines, generation=3):
    # Collect bookmarks and adjust page numbers
    # [granparent,[parent1,[parent2,[son]]]

    # A family is a lsit with the next structure [{parent},[list of childs]], if a individual
    # has child its is defined as a list.

    bookmark_list = []

    family_tree = [outlines]  # Family tree is a list of families
    for i in range(0, generation):
        print(f"GENERATION {i+1}".center(50, "-"))

        for family in family_tree:
            print(family)
            parent, childs = gen_identify(family)
            print(f'"{parent["/Title"]}" has {len(childs)} sons:')
            # Write parent bookmark

            # Analize childs
            next_gen = []
            for child in childs:
                if isinstance(child, dict):
                    print(f'\t"{child["/Title"]}" has no sons')

                    # Write bookmark

                elif isinstance(child, list):
                    print(f'\t"{child[0]["/Title"]}" has {len(child[1])} sons')
                    next_gen.append(child)

        print("next generation size:", len(next_gen))
        print(next_gen)

        family_tree = next_gen

        # _, _ = gen_identify(child)

    # bookmark = {"title": ,"page": ,"parent": }
    # return bookmark_family

    """ for element in outlines:

        if isinstance(element, dict):
            parent = element["/Title"]
            print(parent)

        elif isinstance(element, list):
            sons = element
            for son in sons:
                if isinstance(son, dict):
                    print("\t" + son["/Title"])
                elif isinstance(son, list):
                    grandsons = son
                    for grandson in grandsons:
                        print("\t\t" + grandson["/Title"]) """


def merge_pdfs_with_bookmarks(pdf_files, output_file):
    pdf_writer = PyPDF2.PdfWriter()
    total_pages = 0
    bookmark_list = []

    for pdf_file in pdf_files:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        # Append pages to the writer
        for page_num in range(num_pages):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        bookmarks_family_tree(pdf_reader.outline)

        def collect_bookmarks(outlines, parent=None, parent_pages=0):
            for outline in outlines:
                if isinstance(outline, list):
                    collect_bookmarks(outline, parent, parent_pages)
                else:
                    bookmark_list.append(
                        {
                            "title": outline.title,
                            "page_num": pdf_reader.get_destination_page_number(outline)
                            + total_pages,
                            "parent": parent,
                        }
                    )

        if pdf_reader.outline:
            collect_bookmarks(pdf_reader.outline)

        total_pages += num_pages

    # Add bookmarks to the final PDF
    bookmark_dict = {}
    for bookmark in bookmark_list:
        parent = bookmark_dict.get(bookmark["parent"], None)
        new_bookmark = pdf_writer.add_outline_item(
            title=bookmark["title"], page_number=bookmark["page_num"], parent=parent
        )
        bookmark_dict[bookmark["title"]] = new_bookmark

    # Write out the merged PDF
    with open(output_file, "wb") as out_pdf_file:
        pdf_writer.write(out_pdf_file)


##############################
folder = r"C:\Users\marco\Escritorio\The Analytical Chemestry of Cannabis"
output_file = "merged_book_with_bookmarks.pdf"

""" # get pdf list in folder
pdf_files = []
for pdf in os.listdir(folder):
    if pdf.lower().endswith(".pdf"):
        pdf_files.append(os.path.join(folder, pdf))
        print(pdf) """

pdf_files = (
    r"C:\Users\marco\Escritorio\The Analytical Chemestry of Cannabis\Chapter1.pdf",
    r"C:\Users\marco\Escritorio\The Analytical Chemestry of Cannabis\Chapter2.pdf",
)

print(f"There are {len(pdf_files)} in folder")

merge_pdfs_with_bookmarks(pdf_files, output_file)
