var util = (function() {

    function renderToMarkdown($dom) {
        $dom.html(marked($dom.text()));
    }

    function showLocalTime($dom) {
        var utcDate = moment.utc($dom.attr('datetime'));
        var localDate = utcDate.local().format("dddd, MMMM Do YYYY, h:mm A");
        $dom.text(localDate);
        return localDate;
    }

    return {
        renderToMarkdown: renderToMarkdown,
        showLocalTime: showLocalTime
    };
})();