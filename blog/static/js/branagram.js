/*
Template Name: VIDOE - Video Streaming Website HTML Template
Author: Askbootstrap
Author URI: https://themeforest.net/user/askbootstrap
Version: 1.0
*/
(function($) {
    "use strict"; // Start of use strict

    // Toggle the side navigation
    $(document).on('click', '#sidebarToggle', function(e) {
        e.preventDefault();
        $("body").toggleClass("sidebar-toggled");
        $(".sidebar").toggleClass("toggled");
    });
    $(document).ready(function() {
        function screenClass() {
            if ($(window).innerWidth() > 575) {
                $(".sidebar").hover(function(e) {
                    $("body").removeClass("sidebar-toggled");
                    $(".sidebar").removeClass("toggled");
                });
                $("#content").hover(function(e) {
                    $("body").addClass("sidebar-toggled");
                    $(".sidebar").addClass("toggled");
                });
            } else {
                $("body").addClass("sidebar-toggled");
                $(".sidebar").addClass("toggled");
            }
        }

        screenClass();

        $(window).bind('resize', function() {
            screenClass();
        });
    });

    // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
    $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
        if ($window.width() > 575) {
            var e0 = e.originalEvent,
                delta = e0.wheelDelta || -e0.detail;
            this.scrollTop += (delta < 0 ? 1 : -1) * 30;
            e.preventDefault();
        }
    });

    // Category Owl Carousel
    var objowlcarousel = $(".owl-carousel-category");
    if (objowlcarousel.length > 0) {
        objowlcarousel.owlCarousel({
            items: 8,
            lazyLoad: true,
            pagination: false,
            loop: true,
            autoPlay: 2000,
            navigation: true,
            stopOnHover: true,
            navigationText: ["<i class='fa fa-chevron-left'></i>", "<i class='fa fa-chevron-right'></i>"]
        });
    }
      // Category Owl Carousel
    var objowlcarousel = $(".owl-carousel-category2");
    if (objowlcarousel.length > 0) {
        objowlcarousel.owlCarousel({
            items: 5,
            lazyLoad: true,
            pagination: false,
            loop: true,
            autoPlay: 2000,
            navigation: true,
            stopOnHover: true,
            navigationText: ["<i class='fa fa-chevron-left'></i>", "<i class='fa fa-chevron-right'></i>"]
        });
    }

    // Login Owl Carousel
    var mainslider = $(".owl-carousel-login");
    if (mainslider.length > 0) {
        mainslider.owlCarousel({
            items: 1,
            lazyLoad: true,
            pagination: true,
            autoPlay: 4000,
            loop: true,
            singleItem: true,
            navigation: false,
            stopOnHover: true,
            navigationText: ["<i class='mdi mdi-chevron-left'></i>", "<i class='mdi mdi-chevron-right'></i>"]
        });
    }

    // Tooltip
    $('[data-toggle="tooltip"]').tooltip()

    // Scroll to top button appear
    $(document).on('scroll', function() {
        var scrollDistance = $(this).scrollTop();
        if (scrollDistance > 100) {
            $('.scroll-to-top').fadeIn();
        } else {
            $('.scroll-to-top').fadeOut();
        }
    });

    // Smooth scrolling using jQuery easing
    $(document).on('click', 'a.scroll-to-top', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top)
        }, 1000, 'easeInOutExpo');
        event.preventDefault();
    });

})(jQuery); // End of use strict