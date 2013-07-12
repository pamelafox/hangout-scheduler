(function($){
    $.fn.extend({

        eventLinker: function(options) {
            var defaults = {
            };

            options = $.extend(defaults, options);

            return this.each(function() {
                var o =options;

                //Assign current element to variable, in this case is UL element
                var $timeEl = $(this);
                if ($timeEl.attr('data-event-linker')) return;

                // Get all the information from data attributes
                var eventDateTime = $timeEl.attr('data-event-dates');
                var eventTitle = $timeEl.attr('data-event-title') || document.title;
                var eventLocation = $timeEl.attr('data-event-location') || window.location.href;
                var eventDescription = $timeEl.attr('data-event-description') || '';
                var calendarUrl = 'https://www.google.com/calendar/render?action=TEMPLATE' +
                                  '&text=' + encodeURIComponent(eventTitle) +
                                  '&dates=' + eventDateTime +
                                  '&details=' + encodeURIComponent(eventDescription.replace(/\s+/g, " ")) +
                                  '&location=' + encodeURIComponent(eventLocation);
                var $calendarLink = $('<a>').attr('href', calendarUrl).attr('target', '_blank');
                $calendarLink.append('Add to calendar');

                var $calendarIcon = $('<span></span>');
                $calendarIcon.css({
                  width: '16px',
                  height: '16px',
                  display: 'inline-block',
                  marginLeft: '6px',
                  marginRight: '6px',
                  verticalAlign: 'middle',
                  backgroundRepeat: 'no-repeat',
                  backgroundImage: 'url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAACT0lEQVQ4y52TT0uUURTGf/e+7zjOWIouDAyKNAvNSkFRslW0cNG6L9AqaB0oQrSwvkGLaNGmVbs+QUWhoZZpNENqoYhhEM447/x97z2nxatWS33gcC6X8+d5DucYVeVfVKtVtra2WFtbI5fLkc/nWV9fZ3Nzk52dHaIowlpLZ2cnPT09mMczD6bS6fQER0StVn85Nf3wSRgEwcTP/lvD9abWTBQrxSimUIwpFBtEpZgocjTqHvFK2GQ4kbWcaymVb9o5DzwP6/VGWCGbiWpCsarsFjx7e55SpFQiqDdACWhuCTnZmqK9zRKmmjLxL5cGMqFzDbtbalCoCMWyZ2/PEZVjqhVP3PAYA5lsSFurob0joKXJkLUhzsUWCMLm5mzw4nYfAKqKiPxn3vtDf/Cu1Wr67CkAJjQWAzC7+BlRRUUQUUQFVUG84MWjonif/A32XwiMVQNgRQRVxQYBo4MDWGsZudqPNYbT54cwxnC2bwSAnitj6H68iAAQeueNqhLHMbOLy3jxzH1aRkXZyM2TmrzPtiqpdJrVyWlE96U5lzDw3lkRwRrDqe6BpHPvEABn+oYB6Bobx2DoHbqeyEtmYgGsc96ICLFzbK8u4Zxj4+s8zsV8X5lDRdmefYeokFt4g6qiqjjnD2aQFLDG0NU7iDF/O3dfHqM284iuV6+pTE0zdOkiqol2kaRA6J23Bww2cwuIeH58+YD3wurSe1SF/OJbRISPK7nDVfYukRCKiMlkMtwYHz3SLYhIwqBcLvt7d+8sc0wY4BrQcYzc38C3P6LVdjoMoJ59AAAAAElFTkSuQmCC)'
                });
                $calendarLink.prepend($calendarIcon);
                $timeEl.append($calendarLink);
                $timeEl.attr('data-event-linker', 'true');
            });
        }
    });
})(jQuery);