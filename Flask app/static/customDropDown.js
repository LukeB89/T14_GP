function createCustomDropDowns() {
    // a function that searches for all 'SELECT' elements in the HTML DOM
    // and replaces them with a custom implementation of a drop-down menu

    // code adapted from solution available at:
    // https://www.w3schools.com/howto/howto_custom_select.asp

    // get an array of all 'custom-select' div elements in the HTML doc
    var dropDowns = document.getElementsByClassName("custom-select");

    // for each individual 'custom-select'
    for (var i = 0; i < dropDowns.length; i++) {

        // get the 'SELECT' element associated with this dropdown
        var select = dropDowns[i].getElementsByTagName("SELECT")[0];

        // create a new DIV that will act as the currently selected option
        var currentSelection = document.createElement("DIV");
        currentSelection.setAttribute("class", "select-selected");

        // set the innerHTML of the 'currently selected' div to be whatever the
        // currently selected option from the parent 'SELECT' element is
        currentSelection.innerHTML = select.options[select.selectedIndex].innerHTML;
        dropDowns[i].appendChild(currentSelection); // add element as a child to this 'custom-select' div

        // create a new DIV that will act as options list
        var options = document.createElement("DIV");
        options.setAttribute("class", "select-items select-hide");

        // for each option in the 'SELECT' elements options;
        // add this option to the 'options' DIV
        for (var j = 1; j < select.length; j++) {
            // create a new DIV that will act as an option item
            item = document.createElement("DIV");
            item.innerHTML = select.options[j].innerHTML;

            // define an 'on-click' function to update the original select box and the selected item
            item.addEventListener("click", function(e) {

                // get the 'SELECT' element corresponding to the the parent SELECT list
                parentSelect = this.parentNode.parentNode.getElementsByTagName("select")[0];
                // get the 'OPTION' element before the current one
                lastOption = this.parentNode.previousSibling;

                // get the index of the corresponding 'OPTION' in the parent 'SELECT'
                // and set that 'OPTION' as bing currently selected
                for (var i = 0; i < parentSelect.length; i++) {
                    if (parentSelect.options[i].innerHTML == this.innerHTML) {
                        parentSelect.selectedIndex = i;

                        lastOption.innerHTML = this.innerHTML;

                        // get the item in the options list that is currently selected
                        var selectedOption = this.parentNode.getElementsByClassName("same-as-selected");

                        // 'deselect' this item
                        for (var k = 0; k < selectedOption.length; k++) {
                            selectedOption[k].removeAttribute("class");
                        }

                        // 'select' the item that was clicked on
                        this.setAttribute("class", "same-as-selected");
                        break;
                    }
                }
                lastOption.click();
            });
            options.appendChild(item);
        }

        dropDowns[i].appendChild(options);

        currentSelection.addEventListener("click", function(elem) {
            /* When the select box is clicked, close any other select boxes,
            and open/close the current select box: */

            elem.stopPropagation();
            closeAllSelect(this);
            this.nextSibling.classList.toggle("select-hide");
            this.classList.toggle("select-arrow-active");

      });
    }
}


function closeAllSelect(elem) {
    /* A function that will close all select boxes in the document,
    except the current select box: */

    // code adapted from solution available at:
    // https://www.w3schools.com/howto/howto_custom_select.asp

    var arrNo = [];
    var x = document.getElementsByClassName("select-items");
    var y = document.getElementsByClassName("select-selected");

    for (var i = 0; i < y.length; i++) {
        if (elem == y[i]) {
            arrNo.push(i)
        } else {
            y[i].classList.remove("select-arrow-active");
        }
    }
    for (i = 0; i < x.length; i++) {
        if (arrNo.indexOf(i)) {
            x[i].classList.add("select-hide");
        }
    }
}

/* If the user clicks anywhere outside the select box,
then close all select boxes: */
document.addEventListener("click", closeAllSelect);