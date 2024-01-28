# Content test enforcer

This is a proof of concept to support the blog post [Testing code examples, but
better](https://frankharkins.github.io/blog/test-code-examples-better/).


## Install

```sh
pip install git+https://github.com/frankharkins/content-test-enforcer.git
```

## Usage

Add comments starting with `#| content:`, followed by markdown that should
appear somewhere in the notebook. To check the markdown does appear in the
notebook, run:

```sh
content-test-enforcer path(s)/to/notebook(s)
```

For examples of content tests, see `test/example-notebooks`.
