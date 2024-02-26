$(function() {

    function id_to_windowname(text) {
        text = text.replace(/\./g, '__dot__');
        text = text.replace(/\_/g, '__dash__');
        return text;
    }

    function windowname_to_id(text) {
        text = text.replace(/__dot__/g, '.');
        text = text.replace(/__dash__/g, '_');
        return text;
    }

    function dismissAddRelatedObjectPopup(win, newId, newRepr) {
        console.log("dismissAddRelatedObjectPopup")
        var name = windowname_to_id(win.name);
        var elem = document.getElementById(name);
        if (elem) {
            var elemName = elem.nodeName.toUpperCase();
            if (elemName === 'SELECT') {
                elem.options[elem.options.length] = new Option(newRepr, newId, true, true);
            } else if (elemName === 'INPUT') {
                if (elem.className.indexOf('vManyToManyRawIdAdminField') !== -1 && elem.value) {
                    elem.value += ',' + newId;
                } else {
                    elem.value = newId;
                }
            }
            // Trigger a change event to update related links if required.
            $(elem).trigger('change');
            $(elem).selectpicker('refresh');
        }
        win.close();
    }


    // Global for testing purposes
    window.id_to_windowname = id_to_windowname;
    window.windowname_to_id = windowname_to_id;
    window.dismissAddRelatedObjectPopup = dismissAddRelatedObjectPopup;

    // Kept for backward compatibility
    window.dismissAddAnotherPopup = dismissAddRelatedObjectPopup;

    $(document).delegate('select', 'change', function(e) {
        e.preventDefault();
        console.log("SELECT CLICKED");
        if ($(this).val() == '-100'){
            $(this).val('');
            myUrl = $(this).find(".create_option").data("url");
            idname = $(this).attr("id");
            console.log('idname: '+idname);
            idname = id_to_windowname(idname);
            console.log('windowname: '+idname);
            var newwindow = window.open(myUrl, idname,'_blank, height=500, width=800, resizable=yes, scrollbars=yes');
            //newwindow.focus();
            console.log(newwindow)
        }else if ($(this).val() == '-200'){
            $(this).val('');
            myUrl = $(this).find(".search_option").data("url");
            idname = $(this).attr("id");
            console.log('idname: '+idname);
            idname = id_to_windowname(idname);
            console.log('windowname: '+idname);
            var newwindow = window.open(myUrl, idname,'_blank, height=500, width=800, resizable=yes, scrollbars=yes');
            //newwindow.focus();
            console.log(newwindow)
        }
    });

})
