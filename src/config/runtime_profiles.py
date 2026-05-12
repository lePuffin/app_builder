RUNTIME_PROFILES = {

    "sandbox": {
        "environment": "docker",
        "headless": True,
        "supports_gui_execution": False,
        "supports_stdin": False,
        "supports_network": True,
    },

    "desktop": {
        "environment": "desktop",
        "headless": False,
        "supports_gui_execution": True,
        "supports_stdin": True,
        "supports_network": True,
    },

    "browser": {
        "environment": "browser",
        "headless": False,
        "supports_gui_execution": True,
        "supports_stdin": False,
        "supports_network": True,
    }
}