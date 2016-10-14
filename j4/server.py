#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas
from flask import Flask, render_template
from jinja2 import Template

# prevent PyCharm from removing these imports, even if unused
assert any([Template, ])

app = Flask(__name__)


def edit(d):
    for x in d.iterrows():
        for y in x[1].keys():
            print("x[1]['{}']".format(y), x[1][y])


def recup_donnes(nomfic):
    d = pandas.read_csv(nomfic)
    # edit(d)
    return d


@app.route("/")
def template_test():
    return render_template('template.html', pandaobject=recup_donnes('donnees.csv'))


if __name__ == "__main__":
    app.run(debug=True)
