__webpack_require__.r(__webpack_exports__);
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
var react_dom__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-dom */
"./node_modules/react-dom/index.js");
/* harmony import */
var react_dom__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/
__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */
var _index_css__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./index.css */
"./src/index.css");
/* harmony import */
var _resize__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./resize */
"./src/resize.tsx");
/* harmony import */
var _model__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./model */
"./src/model.tsx");
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

var FlexibleModal = /*#__PURE__*/
function(_Component) {
    _inherits(FlexibleModal, _Component);

    var _super = _createSuper(FlexibleModal);

    function FlexibleModal(props) {
        var _this;

        _classCallCheck(this, FlexibleModal);

        _this = _super.call(this, props);
        _this.state = {
            isDragging: false,
            isResizing: false,
            top: _this.props.top !== undefined ? _this.props.top : _this.props.initHeight ? window.innerHeight / 2 - _this.props.initHeight / 2 - 50 : window.innerHeight / 2 - 400 / 2 - 50,
            left: _this.props.left !== undefined ? _this.props.left : _this.props.initWidth ? window.innerWidth / 2 - _this.props.initWidth / 2 - 21 : window.innerWidth / 2 - 800 / 2 - 21,
            width: _this.props.initWidth ? _this.props.initWidth : 800,
            height: _this.props.initHeight ? _this.props.initHeight : 400
        };
        _this.updateStateResizing = _this.updateStateResizing.bind(_assertThisInitialized(_this));
        _this.funcResizing = _this.funcResizing.bind(_assertThisInitialized(_this));
        _this.resize = _this.resize.bind(_assertThisInitialized(_this));
        _this.onMouseMove = _this.onMouseMove.bind(_assertThisInitialized(_this));
        _this.onMouseUp = _this.onMouseUp.bind(_assertThisInitialized(_this));
        _this.onMouseDown = _this.onMouseDown.bind(_assertThisInitialized(_this));
        _this.pressKey = _this.pressKey.bind(_assertThisInitialized(_this));
        return _this;
    }

    _createClass(FlexibleModal, [{
        key: "componentDidMount",
        value: function componentDidMount() {
            var disableKeystroke = this.props.disableKeystroke;
            document.addEventListener('mouseup', this.onMouseUp);
            if (!disableKeystroke)
                document.addEventListener('keydown', this.pressKey);
        }
    }, {
        key: "componentWillUnmount",
        value: function componentWillUnmount() {
            var disableKeystroke = this.props.disableKeystroke;

            if (document.removeEventListener) {
                document.removeEventListener('mousemove', this.onMouseMove);
                document.removeEventListener('mouseup', this.onMouseUp);
                if (!disableKeystroke)
                    document.removeEventListener('keydown', this.pressKey);
            }
        }
    }, {
        key: "onMouseDown",
        value: function onMouseDown(e) {
            // only left mouse button
            document.addEventListener('mousemove', this.onMouseMove);
            if (e.button !== 0)
                return;
            var pos = react_dom__WEBPACK_IMPORTED_MODULE_2___default.a.findDOMNode(this.node_modal);

            if (pos) {
                this.setState({
                    isDragging: true,
                    rel: {
                        x: e.pageX - pos.offsetLeft,
                        y: e.pageY - pos.offsetTop
                    }
                });
            }

            e.stopPropagation();
            e.preventDefault();
        }
    }, {
        key: "onMouseUp",
        value: function onMouseUp(e) {
            document.removeEventListener('mousemove', this.onMouseMove);
            this.setState({
                isDragging: false
            });
            this.setState({
                isResizing: false
            });
            e.stopPropagation();
            // e.preventDefault();
        }
    }, {
        key: "onMouseMove",
        value: function onMouseMove(e) {
            var _this$props = this.props
              , disableMove = _this$props.disableMove
              , disableVerticalMove = _this$props.disableVerticalMove
              , disableHorizontalMove = _this$props.disableHorizontalMove;
            var rel = this.state.rel;

            if (this.state.isDragging && rel) {
                if (disableMove) {} else if (disableVerticalMove && disableHorizontalMove) {} else if (!disableVerticalMove && disableHorizontalMove) {
                    this.setState({
                        top: e.pageY - rel.y
                    });
                } else if (disableVerticalMove && !disableHorizontalMove) {
                    this.setState({
                        left: e.pageX - rel.x
                    });
                } else if (!disableVerticalMove && !disableHorizontalMove) {
                    this.setState({
                        left: e.pageX - rel.x,
                        top: e.pageY - rel.y
                    });
                }
            } else if (this.state.isResizing) {
                this.funcResizing(e.clientX, e.clientY);
            } else {
                return;
            }

            e.stopPropagation();
            e.preventDefault();
        }
    }, {
        key: "updateStateResizing",
        value: function updateStateResizing(isResizing) {
            document.addEventListener('mousemove', this.onMouseMove);
            this.setState({
                isResizing: isResizing
            });
        }
    }, {
        key: "funcResizing",
        value: function funcResizing(clientX, clientY) {
            var _this$props2 = this.props
              , mWidth = _this$props2.minWidth
              , mHeight = _this$props2.minHeight
              , disableVerticalResize = _this$props2.disableVerticalResize
              , disableHorizontalResize = _this$props2.disableHorizontalResize;
            var node = react_dom__WEBPACK_IMPORTED_MODULE_2___default.a.findDOMNode(this.node_modal);
            var minWidth = mWidth ? mWidth : 200;
            var minHeight = mHeight ? mHeight : 100;

            if (!disableHorizontalResize && node && clientX > node.offsetLeft + minWidth) {
                this.setState({
                    width: clientX - node.offsetLeft + 16 / 2
                });
            }

            if (!disableVerticalResize && node && clientY > node.offsetTop + minHeight) {
                this.setState({
                    height: clientY - node.offsetTop + 16 / 2
                });
            }
        }
    }, {
        key: "pressKey",
        value: function pressKey(e) {
            var _this$props3 = this.props
              , onRequestClose = _this$props3.onRequestClose
              , disableResize = _this$props3.disableResize
              , disableMove = _this$props3.disableMove
              , disableVerticalMove = _this$props3.disableVerticalMove
              , disableHorizontalMove = _this$props3.disableHorizontalMove;

            if (e.ctrlKey) {
                switch (e.keyCode) {
                case 37:
                    !disableResize && this.setState(function(prevState) {
                        return {
                            width: prevState.width - 20
                        };
                    });
                    break;

                case 38:
                    !disableResize && this.setState(function(prevState) {
                        return {
                            height: prevState.height - 20
                        };
                    });
                    break;

                case 39:
                    !disableResize && this.setState(function(prevState) {
                        return {
                            width: prevState.width + 20
                        };
                    });
                    break;

                case 40:
                    !disableResize && this.setState(function(prevState) {
                        return {
                            height: prevState.height + 20
                        };
                    });
                    break;
                }
            } else {
                switch (e.keyCode) {
                case 27:
                    onRequestClose();
                    break;

                case 37:
                    !disableMove && !disableHorizontalMove && this.setState(function(prevState) {
                        return {
                            left: prevState.left - 20
                        };
                    });
                    break;

                case 38:
                    !disableMove && !disableVerticalMove && this.setState(function(prevState) {
                        return {
                            top: prevState.top - 20
                        };
                    });
                    break;

                case 39:
                    !disableMove && !disableHorizontalMove && this.setState(function(prevState) {
                        return {
                            left: prevState.left + 20
                        };
                    });
                    break;

                case 40:
                    !disableMove && !disableVerticalMove && this.setState(function(prevState) {
                        return {
                            top: prevState.top + 20
                        };
                    });
                    break;
                }
            }
        }
    }, {
        key: "resize",
        value: function resize(width, height) {
            this.setState(function(prevState) {
                return {
                    width: width || prevState.width,
                    height: height || prevState.height
                };
            });
        }
    }, {
        key: "render",
        value: function render() {
            var _this2 = this;

            var _this$props4 = this.props
              , isOpen = _this$props4.isOpen
              , isMinimised = _this$props4.isMinimised
              , onRequestClose = _this$props4.onRequestClose
              , onRequestMinimise = _this$props4.onRequestMinimise
              , onRequestRecover = _this$props4.onRequestRecover
              , disableResize = _this$props4.disableResize
              , className = _this$props4.className
              , onFocus = _this$props4.onFocus;
            return Object(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__["jsxs"])("div", {
                children: [isOpen && !isMinimised && Object(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__["jsx"])("div", {
                    onClick: onRequestMinimise ? onRequestMinimise : onRequestClose,
                    className: "flexible-modal-mask"
                }, void 0), Object(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__["jsxs"])(_model__WEBPACK_IMPORTED_MODULE_5__["default"], Object.assign({
                    className: className,
                    onFocus: onFocus,
                    width: this.state.width,
                    height: this.state.height,
                    top: this.state.top,
                    left: this.state.left,
                    isDragging: this.state.isDragging,
                    onRequestRecover: onRequestRecover,
                    isMinimised: isMinimised,
                    isOpen: isOpen,
                    ref: function ref(node) {
                        _this2.node_modal = node;
                    }
                }, {
                    children: [this.props.children, Object(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__["jsx"])("div", {
                        onMouseDown: this.onMouseDown,
                        className: "flexible-modal-drag-area",
                        style: {
                            width: this.state.width
                        },
                        ref: function ref(dragArea) {
                            _this2.dragArea = dragArea;
                        }
                    }, void 0), Object(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__["jsx"])("div", {
                        onMouseDown: this.onMouseDown,
                        className: "flexible-modal-drag-area-left",
                        style: {
                            height: this.state.height
                        },
                        ref: function ref(dragArea) {
                            _this2.dragArea2 = dragArea;
                        }
                    }, void 0), Object(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__["jsx"])("div", {
                        onMouseDown: this.onMouseDown,
                        className: "flexible-modal-drag-area-bottom",
                        style: {
                            width: this.state.width
                        },
                        ref: function ref(dragArea) {
                            _this2.dragArea3 = dragArea;
                        }
                    }, void 0), Object(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__["jsx"])("div", {
                        onMouseDown: this.onMouseDown,
                        className: "flexible-modal-drag-area-right",
                        style: {
                            height: this.state.height
                        },
                        ref: function ref(dragArea) {
                            _this2.dragArea4 = dragArea;
                        }
                    }, void 0), !disableResize && Object(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__["jsx"])(_resize__WEBPACK_IMPORTED_MODULE_4__["default"], {
                        updateStateResizing: this.updateStateResizing
                    }, void 0)]
                }), void 0)]
            }, void 0);
        }
    }]);

    return FlexibleModal;
}(react__WEBPACK_IMPORTED_MODULE_1__["Component"]);

/* harmony default export */
__webpack_exports__["default"] = (FlexibleModal);
