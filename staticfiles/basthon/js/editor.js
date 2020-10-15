"use strict";

window.editor = (function () {
    var that = window.ace.edit("editor");
    
    /**
     * Initialize the editor's content.
     */
    that.loadScript = function () {
        /* set script from:
           -> query string if submited
           -> local storage if available
           -> default otherwise
        */
        const url = new URL(window.location.href);
        const script = url.searchParams.get('script');
        if( script ) {
            editor.setValue(decodeURIComponent(script));
        } else if( (typeof(localStorage) !== "undefined") && "py_src" in localStorage) {
            editor.setValue(localStorage.py_src);
        } else {
            editor.setValue('for i in range(10):\n\tprint(i)');
        }
        
        editor.scrollToRow(0);
        editor.gotoLine(0);
    };

    /**
     * Initialize the Ace editor.
     */
    that.init = function () {
        editor.session.setMode("ace/mode/python");
        editor.focus();
        
        editor.setOptions({
            'enableLiveAutocompletion': true,
            'highlightActiveLine': false,
            'highlightSelectedWord': true,
            'fontSize': '12pt',
        });
        
        that.loadScript();
    };

    return that;
})();
