#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import (
    Bool, Enum, IntEnum, Unicode, Coerced, Typed, ForwardTyped, observe
)

from enaml.colors import ColorMember
from enaml.core.declarative import d_, d_func
from enaml.fonts import FontMember
from enaml.layout.geometry import Size
from enaml.styling import Stylable

from .toolkit_object import ToolkitObject, ProxyToolkitObject


class ProxyWidget(ProxyToolkitObject):
    """ The abstract definition of a proxy Widget object.

    """
    #: A reference to the Widget declaration.
    declaration = ForwardTyped(lambda: Widget)

    def set_enabled(self, enabled):
        raise NotImplementedError

    def set_visible(self, visible):
        raise NotImplementedError

    def set_background(self, background):
        raise NotImplementedError

    def set_foreground(self, foreground):
        raise NotImplementedError

    def set_font(self, font):
        raise NotImplementedError

    def set_minimum_size(self, minimum_size):
        raise NotImplementedError

    def set_maximum_size(self, maximum_size):
        raise NotImplementedError

    def set_tool_tip(self, tool_tip):
        raise NotImplementedError

    def set_status_tip(self, status_tip):
        raise NotImplementedError

    def ensure_visible(self):
        raise NotImplementedError

    def ensure_hidden(self):
        raise NotImplementedError

    def restyle(self):
        raise NotImplementedError

    def set_focus(self):
        raise NotImplementedError

    def clear_focus(self):
        raise NotImplementedError

    def has_focus(self):
        raise NotImplementedError

    def focus_next_child(self):
        raise NotImplementedError

    def focus_previous_child(self):
        raise NotImplementedError


class Feature(IntEnum):
    """ An IntEnum defining the advanced widget features.

    """
    #: Enables support for custom focus traversal functions.
    FocusTraversal = 0x1

    #: Enables support for focus events.
    FocusEvents = 0x2

    #: Enables support for drag operations.
    Drag = 0x4

    #: Enables support for drop operations.
    Drop = 0x8


class Widget(ToolkitObject, Stylable):
    """ The base class of visible widgets in Enaml.

    """
    #: Whether or not the widget is enabled.
    enabled = d_(Bool(True))

    #: Whether or not the widget is visible.
    visible = d_(Bool(True))

    #: The background color of the widget.
    background = d_(ColorMember())

    #: The foreground color of the widget.
    foreground = d_(ColorMember())

    #: The font used for the widget.
    font = d_(FontMember())

    #: The minimum size for the widget. The default means that the
    #: client should determine an intelligent minimum size.
    minimum_size = d_(Coerced(Size, (-1, -1)))

    #: The maximum size for the widget. The default means that the
    #: client should determine an intelligent maximum size.
    maximum_size = d_(Coerced(Size, (-1, -1)))

    #: The tool tip to show when the user hovers over the widget.
    tool_tip = d_(Unicode())

    #: The status tip to show when the user hovers over the widget.
    status_tip = d_(Unicode())

    #: Set the extra features to enable for this widget. This value must
    #: be provided when the widget is instantiated. Runtime changes to
    #: this value are ignored.
    features = d_(Coerced(Feature.Flags))

    #: A reference to the ProxyWidget object.
    proxy = Typed(ProxyWidget)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe('enabled', 'visible', 'background', 'foreground', 'font',
        'minimum_size', 'maximum_size', 'tool_tip', 'status_tip')
    def _update_proxy(self, change):
        """ Update the proxy widget when the Widget data changes.

        This method only updates the proxy when an attribute is updated;
        not when it is created or deleted.

        """
        # The superclass implementation is sufficient.
        super(Widget, self)._update_proxy(change)

    #--------------------------------------------------------------------------
    # Reimplementations
    #--------------------------------------------------------------------------
    def restyle(self):
        """ Restyle the toolkit widget.

        This method is invoked by the Stylable class when the style
        dependencies have changed for the widget. This will trigger a
        proxy restyle if necessary. This method should not typically be
        called directly by user code.

        """
        if self.proxy_is_active:
            self.proxy.restyle()

    #--------------------------------------------------------------------------
    # Public API
    #--------------------------------------------------------------------------
    def show(self):
        """ Ensure the widget is shown.

        Calling this method will also set the widget visibility to True.

        """
        self.visible = True
        if self.proxy_is_active:
            self.proxy.ensure_visible()

    def hide(self):
        """ Ensure the widget is hidden.

        Calling this method will also set the widget visibility to False.

        """
        self.visible = False
        if self.proxy_is_active:
            self.proxy.ensure_hidden()

    def set_focus(self):
        """ Set the keyboard input focus to this widget.

        FOR ADVANCED USE CASES ONLY: DO NOT ABUSE THIS!

        """
        if self.proxy_is_active:
            self.proxy.set_focus()

    def clear_focus(self):
        """ Clear the keyboard input focus from this widget.

        FOR ADVANCED USE CASES ONLY: DO NOT ABUSE THIS!

        """
        if self.proxy_is_active:
            self.proxy.clear_focus()

    def has_focus(self):
        """ Test whether this widget has input focus.

        FOR ADVANCED USE CASES ONLY: DO NOT ABUSE THIS!

        Returns
        -------
        result : bool
            True if this widget has input focus, False otherwise.

        """
        if self.proxy_is_active:
            return self.proxy.has_focus()
        return False

    def focus_next_child(self):
        """ Give focus to the next widget in the focus chain.

        FOR ADVANCED USE CASES ONLY: DO NOT ABUSE THIS!

        """
        if self.proxy_is_active:
            self.proxy.focus_next_child()

    def focus_previous_child(self):
        """ Give focus to the previous widget in the focus chain.

        FOR ADVANCED USE CASES ONLY: DO NOT ABUSE THIS!

        """
        if self.proxy_is_active:
            self.proxy.focus_previous_child()

    @d_func
    def next_focus_child(self, current):
        """ Compute the next widget which should gain focus.

        When the FocusTraversal feature of the widget is enabled, this
        method will be invoked as a result of a Tab key press or from
        a call to the 'focus_next_child' method on a decendant of the
        owner widget. It should be reimplemented in order to provide
        custom logic for computing the next focus widget.

        ** The FocusTraversal feature must be enabled for the widget in
        order for this method to be called. **

        Parameters
        ----------
        current : Widget or None
            The current widget with input focus, or None if no widget
            has focus or if the toolkit widget with focus does not
            correspond to an Enaml widget.

        Returns
        -------
        result : Widget or None
            The next widget which should gain focus, or None to follow
            the default toolkit behavior.

        """
        return None

    @d_func
    def previous_focus_child(self, current):
        """ Compute the previous widget which should gain focus.

        When the FocusTraversal feature of the widget is enabled, this
        method will be invoked as a result of a Shift+Tab key press or
        from a call to the 'focus_prev_child' method on a decendant of
        the owner widget. It should be reimplemented in order to provide
        custom logic for computing the previous focus widget.

        ** The FocusTraversal feature must be enabled for the widget in
        order for this method to be called. **

        Parameters
        ----------
        current : Widget or None
            The current widget with input focus, or None if no widget
            has focus or if the toolkit widget with focus does not
            correspond to an Enaml widget.

        Returns
        -------
        result : Widget or None
            The previous widget which should gain focus, or None to
            follow the default toolkit behavior.

        """
        return None

    @d_func
    def focus_gained(self):
        """ A method invoked when the widget gains input focus.

        ** The FocusEvents feature must be enabled for the widget in
        order for this method to be called. **

        """
        pass

    @d_func
    def focus_lost(self):
        """ A method invoked when the widget loses input focus.

        ** The FocusEvents feature must be enabled for the widget in
        order for this method to be called. **

        """
        pass

    @d_func
    def drag_data(self):
        """ A method invoked to determine the data to be used in a drag
        operation.

        ** The Drag feature must be enabled for the widget in order for this
        method to be called. **

        Returns:
        --------
        result : tuple
            A tuple of (dtype, data) where dtype and data are both strings.

        """
        return ('', '')

    @d_func
    def drag_image(self):
        """ A method invoked to determine what image should be placed under
        the cursor during a drag operation.

        ** The Drag feature must be enabled for the widget in order for this
        method to be called. **

        Returns:
        --------
        image : Image
            An Enaml image or None.

        """
        return None

    @d_func
    def drag_enter(self, event):
        """ A method invoked when a drag operation enters the widget's bounds.

        ** The Drop feature must be enabled for the widget in order for this
        method to be called. **

        Parameters
        ----------
        event : DragEvent
            The event representing the drag operation.

        """
        pass

    @d_func
    def drag_move(self, event):
        """ A method invoked when a drag operation moves within the widget's
        bounds.

        ** The Drop feature must be enabled for the widget in order for this
        method to be called. **

        Parameters
        ----------
        event : DragEvent
            The event representing the drag operation.

        """
        pass

    @d_func
    def drag_leave(self):
        """ A method invoked when a drag operation leaves the widget's bounds.

        ** The Drop feature must be enabled for the widget in order for this
        method to be called. **

        """
        pass

    @d_func
    def validate_drop(self, dtype):
        """ A method invoked to determine whether a drop operation should be
        allowed on the widget.

        Parameters
        ----------
        dtype : str
            The type of the data.

        Returns
        -------
        A boolean value representing whether the drop operation should be
        allowed or not.

        """
        return True

    @d_func
    def drop(self, event):
        """ A method invoked when a drag operation ends on the widget.

        ** The Drop feature must be enabled for the widget in order for this
        method to be called. **

        Parameters
        ----------
        event : DragEvent
            The event representing the drag operation.

        """
        pass
