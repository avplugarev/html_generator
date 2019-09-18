# <ИМЯ_ТЭГА атрибут1=значение1 атрибут2=значение2>текст внутри</ИМЯ_ТЭГА>

class Tag:
    # описываем конструктор
    def __init__(self, tag, is_single=False):
        # обязателбные сам, название тега, парный или нет
        # название тега
        self.tag = tag
        # одинарный или нет
        self.is_single = is_single

        # дополнительно задается
        # текст между тегами
        self.text = ''
        # состав атрибутов
        self.attributes = {}  # словарь

    def __enter__(self):
        # мы возвращаем сами себя когда входим в контекст
        return self

    def __exit__(self, type, value, traceback):
        # на выходе выводим на экран тэг с содержимым и атрибутами
        attrs = []  # список
        my_attribute = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
            my_attribute.append('{my_attribute}={my_value}'.format(my_attribute=attribute, my_value=value))
        my_attribute = ' '.join(my_attribute)

        if self.is_single:
            # передаем при объявлении класса одинарный или закрытый?
            print('<{tag} {attrs}/>'.format(tag=self.tag, attrs=my_attribute))
        else:
            print('<{tag} {attrs}>{text}</{tag}>'.format(tag=self.tag, attrs=my_attribute, text=self.text))


class ParentTag(Tag):
    def __init__(self, tag, toplevel=False, is_single=False):
        self.tag =tag
        self.text =""
        self.attributes = {}  # словарь

        self.is_single = is_single
        self.toplevel = toplevel
        self.children = []

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.toplevel:
            print("<{tag}>".format(tag=self.tag))
            for child in self.children:
                print(child)
            print("</{tag}>".format(tag=self.tag))

    def __str__(self):
        # на выходе выводим на экран тэг с содержимым и атрибутами
        my_attribute = []  # список
        for attribute, value in self.attributes.items():
            my_attribute.append('{my_attribute}={my_value}'.format(my_attribute=attribute, my_value=value))
        my_attribute = ' '.join(my_attribute)
        if self.children:
            opening = "<{tag}{attrs}>".format(tag=self.tag, attrs=my_attribute)
            internal = "%s"%self.text
            for child in self.children:
                internal += '\n'+str(child)
            ending = "\n</%s>"%self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                # передаем при объявлении класса одинарный или закрытый?
                return ('<{tag} {attrs}/>'.format(tag=self.tag, attrs=my_attribute))
            else:
                return ('<{tag} {attrs}>{text}</{tag}>'.format(tag=self.tag, attrs=my_attribute, text=self.text))

class HTML (ParentTag):
    def __init__(self, tag, is_single, toplevel,  output=None):
        self.tag =tag
        self.text =""
        self.attributes = {}  # словарь
        self.output = output
        self.is_single = is_single
        self.toplevel = toplevel
        self.children = []

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.output == "None":
            print(self, "\n\nВывод завершен")
            return self
        else:
            with open(self.output, "w", encoding="utf-8") as outfile:
                outfile.write(str(self))
                print("Сохранение завершено")
            return self
def mychoice():
    print("Выберите вариант результата:\nСохранить в файл - 1\nВывести на экран - 2")
    choice = int(input())
    if choice == 1:
        format_ = "index.html"
    else:
        format_ = "None"
    return format_

def main():
    with HTML("html", toplevel=True, output=mychoice(), is_single=False) as html:
        with ParentTag("head") as head:
            with ParentTag("title") as title:
                title.text = "hello"
                head.children.append(title)
            html.children.append(head)
        with ParentTag("body") as body:
            with ParentTag("h1") as h1:
                h1.text = "Test"
                h1.attributes['class'] = 'main-text'
                body.children.append(h1)
            with ParentTag('div') as div:
                with ParentTag('p') as p:
                    p.text = 'another test'
                    div.children.append(p)
                with ParentTag("img", is_single=True) as img:
                    img.attributes['src'] = '/icon.png'
                    img.attributes['data-image'] = 'responsive'
                    div.children.append(img)
                body.children.append(div)
            html.children.append(body)
if __name__ == "__main__":
    main()