import csv

input_file = "export2.csv"
output_file = "converted_file.csv"

with open(input_file, mode="r", encoding="utf-8") as infile:
    reader = csv.reader(infile, delimiter="\t")
    rows = list(reader)

processed_rows = []
for row in rows:
    if len(row) >= 5:
        kanji = row[2].strip('"')
        hiragana = row[3].strip('"')
        back = row[4].strip('"')
        processed_rows.append([kanji, hiragana, back])

with open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerows(processed_rows)
