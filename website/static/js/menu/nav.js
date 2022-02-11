// 메뉴 열기
$(".btnMenu").click(function () {
    $(".blackBg").fadeIn(300);
    $(".sideMenu").animate({
        right: 0
    }, 500);
});
// 메뉴 닫기
$(".closeBtn, .blackBg").click(function () {
    $(".blackBg").fadeOut(300);
    $(".sideMenu").animate({
        right: -320
    }, 500);
});

// AOS.init();