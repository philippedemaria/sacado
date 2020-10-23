'use strict';

/**
 * Using the namespace design pattern.
 */
Basthon.Goodies = (function() {
    var that = {};
    
    /**
     * Show a fullscreen loader that diseapear when Baston is loaded.
     */
    that.showLoader = function (text) {
        // dynamically adding the loader to the DOM
        var bg = document.createElement("div");
        bg.style.cssText = `
            position: absolute;
            top: 0px;
            left: 0px;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.65);
            text-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 2000;`;
        var container = document.createElement("div");
        container.style.cssText = `
            display: flex;
            justify-content: center;
            align-items: center;
            flex-wrap: wrap;
            width: 100%;`;
        bg.appendChild(container);
        var loader = document.createElement("div");
        loader.style.cssText = `
            position: relative;
            border: 16px solid #fcc24a;
            border-top: 16px solid #3b749c;
            border-bottom: 16px solid #3b749c;
            border-radius: 50%;
            width: 120px;
            height: 120px;
            animation: spin 2s linear infinite;
            overflow: auto;
            opacity: 0.8;`;
        container.appendChild(loader);
        var lineBreak = document.createElement("div");
        lineBreak.style.cssText = `
            flex-basis: 100%;
            height: 20px;`;
        container.appendChild(lineBreak);
        var textElem = document.createElement("div");
        textElem.innerHTML = text;
        textElem.style.cssText = "color: white;";
        container.appendChild(textElem);

        // global style for spining
        var style = document.createElement("style");
        document.head.appendChild(style);
        style.sheet.insertRule(`
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }`);
        
        document.body.appendChild(bg);
        
        return Basthon.load.then(function () {
            // hiding the loader
            var toHide = Array.prototype.slice.call(bg.children);
            toHide.push(bg);
            toHide.forEach(function (elem) {
                elem.style.display = "none";
            });
        });
    };

    return that;
})();
