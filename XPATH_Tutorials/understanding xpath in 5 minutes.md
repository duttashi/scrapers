## Objective
To learn XPath for web data scraping.

## List of XPaths

- The basic XPath syntax is similar to filesystem addressing. If the path starts with the slash `/` , then it represents an absolute path to the required element.
`/AAA
/AAA/CCC`

- If the path starts with `//` then all elements in the document which fulfill following criteria are selected.
`//BBB
//DDD/BBB` 

- The star `*` selects all elements located by preceeding path
`/AAA/CCC/DDD/*
/*/*/*/BBB`

- Expresion in square brackets can further specify an element. A number in the brackets gives the position of the element in the selected set. The function `last()` selects the last element in the selection.
/AAA/BBB[1]
/AAA/BBB[last()]

- Attributes are specified by `@` prefix.
`//@id
//BBB[@id]
//BBB[@name]
//BBB[@*]
//BBB[not(@*)]`

- Values of attributes can be used as selection criteria. `//BBB[@id='b1']
//BBB[@name='bbb']`

- Function `count()` counts the number of selected elements
`//*[count(BBB)=2]
//*[count(*)=2]
//*[count(*)=3]`

- Function `name()` returns name of the element, the `starts-with()` function returns true if the first argument string starts with the second argument string, and the `contains()` function returns true if the first argument string contains the second argument string.
`//*[name()='BBB']
//*[starts-with(name(),'B')]
//*[contains(name(),'C')]`

- The `string-length()` function returns the number of characters in the string. You must use `&lt;` as a substitute for `<` and `&gt;` as a substitute for > .
`//*[string-length(name()) = 3]
//*[string-length(name()) < 3]
//*[string-length(name()) > 3]`

- Several paths can be combined with `|` separator.
`//CCC | //BBB
/AAA/EEE | //BBB
/AAA/EEE | //DDD/CCC | /AAA | //BBB`

### Testing the XPath

If using Google Chrome then install the `XPath Helper` [addon](https://chrome.google.com/webstore/detail/xpath-helper/hgimnogjllphhhkhlmebbmlgjoejdpjl) written by `Adam Sadovsky` from Chrome Store. Once installed, you may have to restart the browser. 
Now the icon for XPath Helper will appear on the top right most side of the Chrome browser. Just click on it to open the helper. 

### How to locate XPath in a webpage

Browse to a webpage and then right click on the text/image to scrape. Choose, `Inspect Element`. You will see the `html` content for that webpage. From here, you can locate the XPath of the element you're interested in.

### How to use XPath Helper Tool?

*Instructions*:

Open a new tab and navigate to any webpage. Hit `Ctrl-Shift-X` (or `Command-Shift-X` on OS X), or click the XPath Helper button in the toolbar, to open the XPath Helper console.
Hold down `Shift` key as you mouse over elements on the page. The query box will continuously update to show the XPath query for the element below the mouse pointer, and the results box will show the results for the current query.
If desired, edit the XPath query directly in the console. The results box will immediately reflect your changes.
Repeat step (2) to close the console.


*Note: If the console gets in your way, hold down Shift and then move your mouse over it; it will move to the opposite side of the page.*

*One word of caution: When rendering HTML tables, Chrome inserts artificial `<tbody>` tags into the DOM, which will consequently show up in queries extracted by this extension.*

#### Reference

For more details refer to [this page](http://zvon.org/comp/r/tut-XPath_1.html?utm_medium=referral&utm_campaign=ZEEF&utm_source=https%3A%2F%2Fscrapy.zeef.com%2Felias.dorneles#Pages~List_of_XPaths).