__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */
__webpack_require__.d(__webpack_exports__, "default", function() {
    return Modal;
});
/* harmony import */
var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */
"./node_modules/react/jsx-runtime.js");
/* harmony import */
var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/
__webpack_require__.n(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */
var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */
"./node_modules/react/index.js");
/* harmony import */
var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/
__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */
var _index_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./index.css */
"./src/index.css");
/* harmony import */
var react_icons_fa__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react-icons/fa */
"./node_modules/react-icons/fa/index.esm.js");
/* harmony import */
var react_transition_group__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react-transition-group */
"./node_modules/react-transition-group/esm/index.js");
function _typeof(obj) {
    "@babel/helpers - typeof";
    if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") {
        _typeof = function _typeof(obj) {
            return typeof obj;
        }
        ;
    } else {
        _typeof = function _typeof(obj) {
            return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj;
        }
        ;
    }
    return _typeof(obj);
}

function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
        throw new TypeError("Cannot call a class as a function");
    }
}

function _defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
        var descriptor = props[i];
        descriptor.enumerable = descriptor.enumerable || false;
        descriptor.configurable = true;
        if ("value"in descriptor)
            descriptor.writable = true;
        Object.defineProperty(target, descriptor.key, descriptor);
    }
}

function _createClass(Constructor, protoProps, staticProps) {
    if (protoProps)
        _defineProperties(Constructor.prototype, protoProps);
    if (staticProps)
        _defineProperties(Constructor, staticProps);
    return Constructor;
}

function _inherits(subClass, superClass) {
    if (typeof superClass !== "function" && superClass !== null) {
        throw new TypeError("Super expression must either be null or a function");
    }
    subClass.prototype = Object.create(superClass && superClass.prototype, {
        constructor: {
            value: subClass,
            writable: true,
            configurable: true
        }
    });
    if (superClass)
        _setPrototypeOf(subClass, superClass);
}

function _setPrototypeOf(o, p) {
    _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) {
        o.__proto__ = p;
        return o;
    }
    ;
    return _setPrototypeOf(o, p);
}

function _createSuper(Derived) {
    var hasNativeReflectConstruct = _isNativeReflectConstruct();
    return function _createSuperInternal() {
        var Super = _getPrototypeOf(Derived), result;
        if (hasNativeReflectConstruct) {
            var NewTarget = _getPrototypeOf(this).constructor;
            result = Reflect.construct(Super, arguments, NewTarget);
        } else {
            result = Super.apply(this, arguments);
        }
        return _possibleConstructorReturn(this, result);
    }
    ;
}

function _possibleConstructorReturn(self, call) {
    if (call && (_typeof(call) === "object" || typeof call === "function")) {
        return call;
    } else if (call !== void 0) {
        throw new TypeError("Derived constructors may only return object or undefined");
    }
    return _assertThisInitialized(self);
}

function _assertThisInitialized(self) {
    if (self === void 0) {
        throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
    }
    return self;
}

function _isNativeReflectConstruct() {
    if (typeof Reflect === "undefined" || !Reflect.construct)
        return false;
    if (Reflect.construct.sham)
        return false;
    if (typeof Proxy === "function")
        return true;
    try {
        Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {}));
        return true;
    } catch (e) {
        return false;
    }
}

function _getPrototypeOf(o) {
    _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) {
        return o.__proto__ || Object.getPrototypeOf(o);
    }
    ;
    return _getPrototypeOf(o);
}

var Modal = /*#__PURE__*/
function(_Component) {
    _inherits(Modal, _Component);

    var _super = _createSuper(Modal);

    function Modal() {
        _classCallCheck(this, Modal);

        return _super.apply(this, arguments);
    }

    _createClass(Modal, [{
        key: "render",
        value: function render() {
            var _this = this;

            var _this$props = this.props
              , isDragging = _this$props.isDragging
              , width = _this$props.width
              , height = _this$props.height
              , top = _this$props.top
              , left = _this$props.left
              , isOpen = _this$props.isOpen
              , isMinimised = _this$props.isMinimised
              , onRequestRecover = _this$props.onRequestRecover
              , className = _this$props.className
              , onFocus = _this$props.onFocus;

            if (isOpen) {
                return Object(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__["jsxs"])(react__WEBPACK_IMPORTED_MODULE_1__["Fragment"], {
                    children: [Object(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__["jsx"])(react_transition_group__WEBPACK_IMPORTED_MODULE_4__["CSSTransition"], Object.assign({
                        "in": !isMinimised,
                        timeout: 300,
                        classNames: "minimise",
                        unmountOnExit: true
                    }, {
                        children: Object(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__["jsx"])("div", Object.assign({
                            onClick: onFocus,
                            ref: function ref(node) {
                                _this.node = node;
                            },
                            draggable: isDragging,
                            className: !className ? "flexible-modal" : "flexible-modal " + className,
                            style: {
                                width: width,
                                height: height,
                                top: top,
                                left: left
                            }
                        }, {
                            children: this.props.children
                        }), void 0)
                    }), void 0), isMinimised && Object(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__["jsx"])("button", Object.assign({
                        className: "flexible-modal-rebound-btn",
                        onClick: onRequestRecover
                    }, {
                        children: Object(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__["jsx"])(react_icons_fa__WEBPACK_IMPORTED_MODULE_3__["FaBars"], {}, void 0)
                    }), void 0)]
                }, void 0);
            } else {
                return null;
            }
        }
    }]);

    return Modal;
}(react__WEBPACK_IMPORTED_MODULE_1__["Component"]);
