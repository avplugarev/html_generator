class Tag:
    def __init__(self, tag, klass=None, is_single=False, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}

        self.is_single = is_single
        self.children = ""
        attrs = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            self.attributes[attr] = value

        for attribute, value in self.attributes.items():
            if "_" in attribute:
                attribute = attribute.replace("_", "-")
            attrs.append('{}="{}"'.format(attribute, value))

        self.attrs = " ".join(attrs)
        if self.attrs != "":
            self.attrs = " " + self.attrs

    def __enter__(self):
        return self

    def __str__(self, *args):
        self.opening = f"<{self.tag}{self.attrs}>{self.text}"
        self.closing = f"</{self.tag}>"

        if self.is_single:
            return self.opening
        elif self.tag == "p" or self.tag == "title" or self.tag == "h1":
            return self.opening + self.children + self.closing
        else:
            return self.opening + self.children + "\n" + self.closing

    def __iadd__(self, other):

        self.children += ("\n" + str(other))
        return Tag(self.tag, is_single=False, subtag=self.children, **kwargs)

    def __exit__(self, *args):
        return self


class HTML(Tag):
    def __init__(self, output="None"):

        self.output = output
        self.tag = "html"
        self.attrs = ""
        self.text = ""
        self.is_single = False
        self.children = ""

    def __exit__(self, *args):

        if self.output == "None":
            print(self, "\n\nВывод завершен")
            return self
        else:
            with open(self.output, "w", encoding="utf-8") as outfile:
                outfile.write(str(self))
                print("Сохранение завершено")
            return self

class TopLevelTag(Tag):
    is_single = False

def mychoice():
    print("Выберите вариант результата:\nСохранить в файл - 1\nВывести на экран - 2")
    choice = int(input())
    if choice == 1:
        format_ = "index.html"
    else:
        format_ = "None"
    return format_

def main():
    with HTML(output=mychoice()) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head
        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1
            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph
                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img
                body += div
            doc += body

if __name__ == "__main__":
    main()