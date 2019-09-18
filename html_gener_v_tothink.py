class TopLevelTag:
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.children = []

    def __iadd__(self, other): #Используем конструкцию += для добавления детей.Нам понадобится специальный метод __iadd__Метод для сложения объектов
        self.children.append(other)
        return self
    #Так как это контекстный менеджер, мы определяем методы __enter__ и __exit__, которые возвращают
    # сам объект при входе в контекст (будет доступен как переменная в конструкции with ... as ...) и ничего не делают при выходе.
    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        #превращаем обхект в строку Используем конструкцию += для добавления детей оипсан выше в метод __iadd__
        html = "<%s>\n" % self.tag
        for child in self.children:
            html += str(child)
        html += "\n</%s>" % self.tag
        return html

class HTML:
    def __init__(self, output=None):
        self.output = output
        self.children = []
        #Так как мы знаем tag, нам не нужен параметр tag в конструкторе.

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        #Вывод результата мы делаем на выходе из контекста, поэтому вся эта логика внутри соответствующего специального метода __exit__
        if self.output is not None:
            with open(self.output, "w") as fp:
                fp.write(str(self))
        else:
            print(self)

    def __str__(self):
        #Вывод идет через преобразование объекта к строке, поэтому вся эта логика и обход детей у нас
        # происходит внутри специального метода __str__
        html = "<html>\n"
        for child in self.children:
            html += str(child)
        html += "\n</html>"
        return html

class Tag:
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}

        self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        return self

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if len(self.children) > 0:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            if self.text:
                internal = "%s" % self.text
            else:
                internal = ""
            for child in self.children:
                internal += str(child)
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return  "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)
            else:
                return "<{tag} {attrs}>{text}</{tag}>".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )

def main(output=None):
    #в качестве параметра на вход задаем как выводим на печать или в файл
    with HTML(output=output) as doc: #класс html (контекстный менеджер) пишет в начале и конце теги и передает свое
                                    # содержимое на экран или в файл Задача других объектов внутри этого контекста —
                                    # добавлять в это поле с html-документом себя (свои тэги с содержимым)
        with TopLevelTag("head") as head: #контекстные менеджеры. Задача этих тэгов — хранить все добавленноев них
            with Tag("title") as title: #конструкторе указываются все их атрибуты и при выходе добавляем в нам род тег как детей.
                title.text = "hello"
                head += title #хранить все добавленноев них
            doc += head #дописывать в общий html-документ объекта класса HTML содержимое (себя и своих "детей")

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag(
                    "img", is_single=True, src="/icon.png", data_image="responsive"
                ) as img:
                    div += img

                body += div

            doc += body
if __name__ == "__main__":
    main()
#with Tag("title") as title:  # конструкторе указываются все их атрибуты и при выходе добавляем в нам род тег как детей.
 #   title.text = "hello"
