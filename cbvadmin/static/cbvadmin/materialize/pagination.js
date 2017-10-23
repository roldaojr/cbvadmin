// based on
// https://github.com/shtalinberg/django-el-pagination/blob/3.1.0/el_pagination/static/el-pagination/js/el-pagination.js
'use strict';

(function ($) {

    // Fix JS String.trim() function is unavailable in IE<9 #45
    if (typeof(String.prototype.trim) === "undefined") {
         String.prototype.trim = function() {
             return String(this).replace(/^\s+|\s+$/g, '');
         };
    }

    $.fn.endlessPaginate = function(options) {
        var defaults = {
            // Twitter-style pagination container selector.
            containerSelector: '.endless_container',
            // Twitter-style pagination loading selector.
            loadingSelector: '.endless_loading',
            // Twitter-style pagination link selector.
            moreSelector: 'a.endless_more',
            // Twitter-style pagination content wrapper selector.
            contentSelector: '.endless-table tbody',
            // Callback called when the user clicks to get another page.
            onClick: function() {},
            // Callback called when the new page is correctly displayed.
            onCompleted: function() {},
            // Set this to true to use the paginate-on-scroll feature.
            paginateOnScroll: true,
            // If paginate-on-scroll is on, this margin will be used.
            paginateOnScrollMargin : 1,
            // If paginate-on-scroll is on, it is possible to define chunks.
            paginateOnScrollChunkSize: 0
        }
        var settings = $.extend(defaults, options)

        var getContext = function(link) {
            return {
                //key: link.data("el-querystring-key").split(' ')[0],
                url: link.attr('href')
            };
        };

        return this.each(function() {
            var element = $(this),
                loadedPages = 1;

            // Twitter-style pagination.
            element.on('click', settings.moreSelector, function(event) {
                event.preventDefault();
                var link = $(this),
                    html_link = link.get(0),
                    content_wrapper = element.find(settings.contentSelector),
                    container = link.closest(settings.containerSelector),
                    loading = container.find(settings.loadingSelector);
                // Avoid multiple Ajax calls.
                if (loading.is(':visible')) {
                    return false;
                }
                link.hide();
                loading.show();
                var context = getContext(link);
                // Fire onClick callback.
                if (settings.onClick.apply(html_link, [context]) !== false) {
                    var data = 'querystring_key=' + context.key;
                    // Send the Ajax request.
                    $.get(context.url, data, function(fragment) {
                        // Increase the number of loaded pages.
                        loadedPages += 1;

                        var rows = $(fragment).find("tbody tr")

                        // Insert the content in the specified wrapper and increment link
                        content_wrapper.append(rows);
                        var nextPage = 'page=' + (loadedPages + 1);
                        link.attr('href', link.attr('href').replace(/page=\d+/, nextPage));
                        link.show();
                        loading.hide();

                        // Fire onCompleted callback.
                        settings.onCompleted.apply(
                            html_link, [context, fragment.trim()]);
                    }).fail(function(xhr, textStatus, error) {
                        // Remove the container left if any
                        container.remove();
                    });
                }
                return false;
            });

            // On scroll pagination.
            if (settings.paginateOnScroll) {
                var win = $(window),
                    doc = $(document);
                doc.scroll(function(){
                    if (doc.height() - win.height() -
                        win.scrollTop() <= settings.paginateOnScrollMargin) {
                        // Do not paginate on scroll if chunks are used and
                        // the current chunk is complete.
                        var chunckSize = settings.paginateOnScrollChunkSize;
                        if (!chunckSize || loadedPages % chunckSize) {
                            element.find(settings.moreSelector).click();
                        } else {
                            element.find(settings.moreSelector).addClass('endless_chunk_complete');
                        }
                    }
                });
            }
        });
    };

    $.endlessPaginate = function(options) {
        return $('body').endlessPaginate(options);
    };

})(jQuery);

$(document).ready(function(){
    $("body").endlessPaginate()
})
