function handleOnChange(e) {
    const value = e.value;

    if (value == "UPBIT") {
        $(".announcement").show();
        $(".passphrase").hide();
    } else if (value == "BITMEX") {
        $(".announcement").hide();
        $(".passphrase").hide();
    } else {
        $(".announcement").hide();
        $(".passphrase").show();
    }

}

