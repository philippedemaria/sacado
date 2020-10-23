'use strict';

/**
 * Using the namespace design pattern.
 */
var Basthon = (function() {
    var that = {};

    /**
     * Where to find pyodide.js (private).
     */
    that._pyodideUrl = "https://pyodide-cdn2.iodide.io/v0.15.0/full/pyodide.js";

    /**
     * Dirname remove basename/filename from url.
     */
    that.dirname = function (url) {
        return url.substring(0, url.lastIndexOf("/"));
    };

    /**
     * Is Basthon loaded ?
     */
    that.loaded = false;

    /**
     * Get the URL of the current script (usefull for serving basthon.py)
     */
    that.urlScript = document.currentScript.src;

    /**
     * Get the URL of Basthon kernel root dir.
     */
    that.basthonRoot = that.dirname(that.urlScript);

    /**
     * A separate namespace for packages (module) managment.
     * (defined here since we need basthonRoot)
     */
    that.packages = (function () {
        var pkg = {};

        /**
         * Available packages in Pyodide.
         * :type: set
         */
        pkg.pyodide = null;

        /**
         * Packages not implemented in Pyodide but in Basthon
         * (dict pointing to Pypi or internal addresse).
         * :type: dict
         */
        pkg.internal = {
            "turtle": {
                path: that.basthonRoot + "/turtle-0.0.1-py3-none-any.whl",
            },
            "requests": {
                path: that.basthonRoot + "/requests-0.0.1-py3-none-any.whl",
            },
            "proj4py": {
                path: that.basthonRoot + "/proj4py-0.0.1-py3-none-any.whl",
                deps: ["pkg_resources"],
            },
            "folium": {
                path: "folium", // loaded from PyPi
            },
        };
        
        /**
         * Union of internal and pyodide packages.
         * :type: set
         */
        pkg.all = null;

        /**
         * Packages already loaded.
         * :type: set
         */
        pkg.loaded = null;

        /**
         * Init packages lists.
         */
        pkg.init = function () {
            pkg.pyodide = new Set(Object.keys(pyodide._module.packages.import_name_to_package_name));
            pkg.all = new Set([...pkg.pyodide, ...Object.keys(pkg.internal)]);
            pkg.loaded = new Set(); // empty (nothing loaded)
        };

        /**
         * Processing packages before loading
         * (common part of Pyodide/internal loading).
         */
        pkg._processPackagesBeforeLoad = function (packages) {
            if( typeof packages === "string" ) {
                packages = [packages];
            }
            // remove already loaded
            packages = packages.filter(p => !pkg.loaded.has(p));
            // updating loaded list
            packages.forEach(p => pkg.loaded.add(p));
            return packages
        };
        
        /**
         * Loading Pyodide packages.
         * Callback function is called on not already loaded packages.
         */
        pkg.loadPyodide = function (packages, callback) {
            packages = pkg._processPackagesBeforeLoad(packages);
            if( packages.length === 0 ) { return Promise.resolve(); }
            // from Python name to Pyodide name
            const pyodidePackages = packages.map(
                p => pyodide._module.packages.import_name_to_package_name[p]);
            return pyodide.loadPackage(pyodidePackages)
                .then(function () { callback(packages); });
        };
        
        /**
         * Loading internal module with micropip (async).
         * Callback function is called on not already loaded packages.
         */
        pkg.loadInternal = function (packages, callback) {
            packages = pkg._processPackagesBeforeLoad(packages);
            if( packages.length === 0 ) { return Promise.resolve(); }
            const packageList = "['" + packages.map(p => pkg.internal[p].path).join("', '") + "']";
            return pyodide.runPythonAsync(
                "import micropip; micropip.install(" + packageList + ")"
            ).then(function () { callback(packages); });
        };
        
        /**
         * Loading module (internal or Pyodide).
         * Callback function is called twice.
         * First on (not already loaded) Pyodide packages,
         * then on (not already loaded) internal packages. 
         */
        pkg.load = function (packages, callback) {
            if( typeof packages === "string" ) {
                packages = [packages];
            }
            if( packages.length === 0 ) {
                return;
            }
            const pyodidePackages = packages.filter(p => pkg.pyodide.has(p));
            const internalPackages = packages.filter(p => p in pkg.internal);
            return pkg.loadPyodide(pyodidePackages, callback)
                .then(function () { return pkg.loadInternal(internalPackages, callback); });
        };
        
        return pkg;
    })();

    /**
     * Dynamically load a script through a promise.
     */
    that.loadScript = function (url) {
        return new Promise(function(resolve, reject) {
            var script = document.createElement('script');
            script.onload = resolve;
            script.onerror = reject;
            script.src = url;
            document.head.appendChild(script);
        });
    };

    /**
     * What to do when loaded (private).
     */
    that._onload = function() {
        that.loaded = true;
        // connecting eval to basthon.eval.request event.
        that.addEventListener("eval.request", that.evalFromEvent);
        // get the version of Python from Python
        const sys = pyodide.pyimport("sys");
        that.pythonVersion = sys.version;
        that.packages.init();
        // reading basthon.py from same folder than current script
        return pyodide.runPythonAsync(
            "import pyodide ; pyodide.eval_code(pyodide.open_url('"
                + that.basthonRoot + "/basthon.py.js').getvalue(), globals())");
    };

    /**
     * Start the Basthon kernel through a promise.
     */
    that.load = (function () {
        // Pyodide launch starts once page is loaded
        var promise = new Promise(function (resolve, reject) {
            window.addEventListener("load", resolve);
        });
        // avoid conflict with requirejs and use it when available.
        promise = promise.then(function () {
            return new Promise(function (resolve, reject) {
                if( typeof requirejs !== 'undefined' ) {
                    resolve();
                } else {
                    reject();
                }
            });
        });

        promise = promise
            .then(function () {
                requirejs.config({paths: {pyodide: that._pyodideUrl.slice(0, -3)}});
                return new Promise(function (resolve, reject) {
                    require(['pyodide'], resolve, reject);
                });
            }, function () {
                return that.loadScript(that._pyodideUrl);
            });

        return promise.then(function () {
            return languagePluginLoader.then(
                that._onload,
                function() { console.error("Can't load Python from Pyodide"); });
        }, function() { console.error("Can't load pyodide.js"); });
    })();

    /**
     *  Ease the creation of events.
     */
    that.dispatchEvent = function (eventName, data) {
        const event = new CustomEvent("basthon." + eventName, { detail: data });
        document.dispatchEvent(event);
    };

    /**
     * Ease the event processing.
     */
    that.addEventListener = function (eventName, callback) {
        document.addEventListener(
            "basthon." + eventName,
            function (event) { callback(event.detail); });
    };

    /**
     * Find modules to import from Python codes.
     */
    that.findImports = function (code) {
        if( !that.loaded ) { return ; }
        var imports = pyodide.globals.pyodide.find_imports(code);
        // manually update internal packages dependencies
        for( const i of imports ) {
            imports = imports.concat(
                (that.packages.internal[i] || {deps: []}).deps);
        }
        return imports;
    };

    /**
     * Cloning function.
     */
    that.clone = function (obj) {
        // simple trick that is enough for our purpose.
        return JSON.parse(JSON.stringify(obj));
    };
    
    /**
     * Basthon simple code evaluation function (not async).
     */
    that.eval = function (code, data=null) {
        if( !that.loaded ) { return ; }
        return pyodide.globals.Basthon.eval(code, data);
    };

    /**
     * Basthon async code evaluation function returning a promise.
     */
    that.evalAsync = function (code, outCallback, errCallback,
                               loadPackageCallback, data=null) {
        if( !that.loaded ) { return ; }
        if( typeof outCallback === 'undefined' ) {
            outCallback = function (text) { console.log(text); };
        }
        if( typeof errCallback === 'undefined' ) {
            errCallback = function (text) { console.error(text); };
        }

        return new Promise(function (resolve, reject) {
            /*
               finding packages, loading, (hacking mpl, turtle and sympy),
               then running
            */
            resolve(that.findImports(code));
        }).then(function(toLoad) {
            return that.packages.load(toLoad, loadPackageCallback);
        }).then(function () {
            return new Promise(function (resolve, reject) {
                resolve(pyodide.globals.Basthon.shell_eval(
                    code, outCallback, errCallback, data));
            });
        });
    };

    /**
     * Basthon evaluation function callback.
     * It is not used directly but through basthon.eval.request event.
     * A Python error throw basthon.eval.error event.
     * Output on stdout/stderr throw basthon.eval.output.
     * Matplotlib display throw basthon.eval.display event.
     * When computation is finished, basthon.eval.finished is thrown.
     */
    that.evalFromEvent = function (data) {
        if( !that.loaded ) { return ; }

        var stdCallback = function (std) { return function (text) {
            var dataEvent = that.clone(data);
            dataEvent.stream = std;
            dataEvent.content = text;
            that.dispatchEvent("eval.output", dataEvent);
        }};
        var outCallback = stdCallback("stdout");
        var errCallback = stdCallback("stderr");
        var loadPackageCallback = function (toLoad) {
            var hack = function (display_data) {
                // execution_count not used here so useless.
                Basthon.dispatchEvent("eval.display", display_data);
            };

            if( toLoad.includes("matplotlib") ) {
                pyodide.globals.Basthon.hack_matplotlib(hack);
            } else if ( toLoad.includes("turtle") ) {
                pyodide.globals.Basthon.hack_turtle(hack);
            } else if ( toLoad.includes("sympy") ) {
                pyodide.globals.Basthon.hack_sympy(hack);
            } else if ( toLoad.includes("folium") ) {
                pyodide.globals.Basthon.hack_folium(hack);
            } else if ( toLoad.includes("pandas") ) {
                pyodide.globals.Basthon.hack_pandas(hack);
            }
        };

        return that.evalAsync(data.code, outCallback, errCallback,
                              loadPackageCallback, data)
            .then(
                function (result) {
                var dataEvent = that.clone(data);
                dataEvent.execution_count = that.executionCount();
                if( typeof result !== 'undefined' ) {
                    dataEvent.result = result;
                }
                that.dispatchEvent("eval.finished", dataEvent);
            },
            function (error) {
                errCallback(error.toString());
                var dataEvent = that.clone(data);
                dataEvent.error = error;
                dataEvent.execution_count = that.executionCount();
                that.dispatchEvent("eval.error", dataEvent);
            });
    };

    /**
     * Get the current execution count.
     */
    that.executionCount = function () {
        return pyodide.globals.Basthon.execution_count;
    };

    /**
     * Restart the kernel.
     */
    that.restart = function () {
        if( !that.loaded ) { return ; }
        return pyodide.globals.Basthon.restart();
    };

    return that;
})();
