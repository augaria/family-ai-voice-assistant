# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.2.0
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

from sys import version_info as _swig_python_version_info  # noqa: F401
# Import the low-level C/C++ module

import builtins as __builtin__

import platform
architecture = platform.machine()
if architecture == 'x86_64' or architecture == 'amd64':
    from .amd64 import _snowboydetect
elif architecture == 'aarch64' or architecture == 'arm64':
    from .arm64 import _snowboydetect


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (
        self.__class__.__module__,
        self.__class__.__name__,
        strthis,
    )


def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "this":
            set(self, name, value)
        elif name == "thisown":
            self.this.own(value)
        elif hasattr(self, name) and isinstance(
            getattr(type(self), name),
            property
        ):
            set(self, name, value)
        else:
            raise AttributeError(
                "You cannot add instance attributes to %s" % self)
    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr


def _swig_add_metaclass(metaclass):
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper


class _SwigNonDynamicMeta(type):
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


class SnowboyDetect(object):
    thisown = property(lambda x: x.this.own(), lambda x,
                       v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, resource_filename, model_str):
        _snowboydetect.SnowboyDetect_swiginit(
            self, _snowboydetect.new_SnowboyDetect(
                resource_filename,
                model_str
            )
        )

    def Reset(self):
        return _snowboydetect.SnowboyDetect_Reset(self)

    def RunDetection(self, *args):
        return _snowboydetect.SnowboyDetect_RunDetection(self, *args)

    def SetSensitivity(self, sensitivity_str):
        return _snowboydetect.SnowboyDetect_SetSensitivity(
            self,
            sensitivity_str
        )

    def SetHighSensitivity(self, high_sensitivity_str):
        return _snowboydetect.SnowboyDetect_SetHighSensitivity(
            self,
            high_sensitivity_str
        )

    def GetSensitivity(self):
        return _snowboydetect.SnowboyDetect_GetSensitivity(self)

    def SetAudioGain(self, audio_gain):
        return _snowboydetect.SnowboyDetect_SetAudioGain(self, audio_gain)

    def UpdateModel(self):
        return _snowboydetect.SnowboyDetect_UpdateModel(self)

    def NumHotwords(self):
        return _snowboydetect.SnowboyDetect_NumHotwords(self)

    def ApplyFrontend(self, apply_frontend):
        return _snowboydetect.SnowboyDetect_ApplyFrontend(self, apply_frontend)

    def SampleRate(self):
        res = _snowboydetect.SnowboyDetect_SampleRate(self)
        print(f"[[[SampleRate: {res}]]]")
        return res

    def NumChannels(self):
        return _snowboydetect.SnowboyDetect_NumChannels(self)

    def BitsPerSample(self):
        return _snowboydetect.SnowboyDetect_BitsPerSample(self)
    __swig_destroy__ = _snowboydetect.delete_SnowboyDetect


# Register SnowboyDetect in _snowboydetect:
_snowboydetect.SnowboyDetect_swigregister(SnowboyDetect)


class SnowboyVad(object):
    thisown = property(lambda x: x.this.own(), lambda x,
                       v: x.this.own(v), doc="The membership flag")
    __repr__ = _swig_repr

    def __init__(self, resource_filename):
        _snowboydetect.SnowboyVad_swiginit(
            self, _snowboydetect.new_SnowboyVad(resource_filename))

    def Reset(self):
        return _snowboydetect.SnowboyVad_Reset(self)

    def RunVad(self, *args):
        return _snowboydetect.SnowboyVad_RunVad(self, *args)

    def SetAudioGain(self, audio_gain):
        return _snowboydetect.SnowboyVad_SetAudioGain(self, audio_gain)

    def ApplyFrontend(self, apply_frontend):
        return _snowboydetect.SnowboyVad_ApplyFrontend(self, apply_frontend)

    def SampleRate(self):
        return _snowboydetect.SnowboyVad_SampleRate(self)

    def NumChannels(self):
        return _snowboydetect.SnowboyVad_NumChannels(self)

    def BitsPerSample(self):
        return _snowboydetect.SnowboyVad_BitsPerSample(self)
    __swig_destroy__ = _snowboydetect.delete_SnowboyVad


# Register SnowboyVad in _snowboydetect:
_snowboydetect.SnowboyVad_swigregister(SnowboyVad)
