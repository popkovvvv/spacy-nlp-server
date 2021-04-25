import random

import srsly
import typer

labels = ['__label__NORMAL', '__label__INSULT', '__label__THREAT', '__label__OBSCENITY']


def save_data(TRAIN_DATA, output_path):
    data = []
    for num, line in enumerate(TRAIN_DATA, start=1):
        data.append({
            "text": line[0]["text"],
            "cats": line[1]["cats"],
            "meta": {"id": num}
        })
    srsly.write_jsonl(output_path, data)


def convert(dataset_path, split, output_path_train, output_path_valid):
    (train_texts, train_cats), (dev_texts, dev_cats) = load_data(dataset_path, split, labels)
    train_data = list(zip([{'text': texts} for texts in train_texts],
                          [{'cats': cats} for cats in train_cats]))

    valid_data = list(zip([{'text': texts} for texts in dev_texts],
                          [{'cats': cats} for cats in dev_cats]))

    save_data(train_data, output_path_train)
    save_data(valid_data, output_path_valid)


def load_data(dataset_path, split, labels):
    data_list = []
    with open(dataset_path) as file:
        for line in file:
            label = line.split()[0]
            text = line.replace(label, "").strip()

            data_list.append((text, label))
    train_data = data_list
    # Shuffle the data
    random.shuffle(train_data)
    texts, labels_data = zip(*train_data)
    # get the categories for each review
    cats = []
    for num, label_data in enumerate(labels_data, start=1):
        category_dict = {}
        for label in labels:
            if label_data == label:
                category_dict[label] = 1.0
            else:
                category_dict[label] = 0.0
        cats.append(category_dict)

    split = int(split)

    # Splitting the training and evaluation data
    return (texts[:split], cats[:split]), (texts[split:], cats[split:])


if __name__ == "__main__":
    typer.run(convert)
