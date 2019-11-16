/**
 * llb datepicker widget
 *
 * @description:  An extension of jquery UI datepicker
 *  that is keyboard accessible and will have
 *  aria labels for accessibility
 *
 * @example:
 * require(['datepicker-widget'], function(datepicker) {
 *   datepicker.addDatePicker($(dateInputSelector), {
 *      minDate: -731,
 *      maxDate: '+0d'
 *   });    
 * });
 *
 */
define('datepicker-widget', [
    'jquery.datepicker'
], function() {
    'use strict';

    //holds datepicker settings
    var settings;

    //holds datepicker container dom
    var $datepicker;

    //holds datepicer input dom
    var $dateInput;

    //keycodes vault
    var keyCode;

    //document dom
    var $doc = $(document);

    //holds day names in an array
    var dayNamesArr = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    //holds month names
    var monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

    //default settings
    var defaults;

    //current module
    var module = {};

    /*
     * Returns full month name
     */
    function getMonth($calendar) {
        var $monthSel = $calendar.find('.ui-datepicker-month');
        if ($monthSel.length) {
            if ($monthSel.is('select')) {
                return monthNames[+$monthSel.val()];
            }

            return $monthSel.text();
        }
    }

    /*
     * Returns year
     */
    function getYear($calendar) {
        var $yearSel = $calendar.find('.ui-datepicker-year');
        if ($yearSel.length) {
            if ($yearSel.is('select')) {
                return $yearSel.val();
            }

            return $yearSel.text();
        }
    }

    /* Set href to previous and next so that keyboard 
     * navigation works find
     */
    function populateAriaAttributes() {
        //need to add some delay as attributes should be set
        //after the datepicker is rendered
        setTimeout(function() {
            var $calendars = $datepicker;
            var $focusElem = $(module.clickedSelector || '.ui-state-active');

            if (settings.numberOfMonths > 1) {
                $calendars = $datepicker.find('.ui-datepicker-group');
            }

            $calendars.each(function() {
                var $calendar = $(this);
                var year = getYear($calendar);
                var month = getMonth($calendar);

                //add href so prev/next links are selectable
                $calendar.find('a.ui-corner-all')
                    .not('.ui-state-disabled')
                    .attr({
                        href: 'javascript:void(0);',
                        role: 'button'
                    })
                    //remove title attribue as we 
                    //set informative text
                    .removeAttr('title')
                    //set inforamtive text for prev/next spans
                    .each(function() {
                        var $a = $(this);
                        var txt = month + ' ' + year;
                        if ($a.data('handler') === 'prev') {
                            txt = 'Previous Month, ' + txt;
                        } else if ($a.data('handler') === 'next') {
                            txt = 'Next Month, ' + txt;
                        }

                        $a.find('.ui-icon').text(txt);
                    });

                //set role on table
                $datepicker.find('table').attr('role', 'grid');

                //set aria-label with informative text for each date
                $calendar.find('a.ui-state-default').each(function() {
                    var $eaDate = $(this);
                    var $tr = $eaDate.parent();
                    var dt = $eaDate.text();
                    var day = dayNamesArr[$tr.index()];

                    $eaDate.attr({
                        'data-date': dt,
                        'data-month': $tr.data('month'),
                        'data-year': $tr.data('year'),
                        'aria-label': month + ' ' + dt + ' ' + year + ' ' + day
                    });
                });
            });


            if (!$focusElem.length) {
                $focusElem = $datepicker.find('.ui-datepicker-calendar .ui-state-default');
            }

            $focusElem.focus();

            delete module.clickedSelector;

        }, 10);
    }

    /*
     * Attach event handlers
     */
    function attachEventHandlers() {
        keyCode = $.ui.keyCode;

        $('.ui-datepicker-trigger').on('click', function() {
            populateAriaAttributes();
        });

        //keydown event handler for canlendar dates
        $datepicker.on('keydown', '.ui-datepicker-calendar a', function(e) {
            var which = e.which;
            var $a = $(this);
            var date = $a.data('date');
            var month = $a.data('month');
            var year = $a.data('year');
            var newDate;
            var $newDt;

            if (date) {
                date = +date;
                month = +month;

                if (keyCode.RIGHT === which) {
                    newDate = date + 1;
                } else if (keyCode.DOWN === which) {
                    newDate = date + 7;
                } else if (keyCode.UP === which) {
                    newDate = date - 7;
                } else if (keyCode.LEFT === which) {
                    newDate = date - 1;
                }

                $newDt = $datepicker.find('a[data-month="' + month + '"][data-date="' + newDate + '"]');

                if ($newDt.length) {
                    e.preventDefault();

                    $newDt.focus();
                } else {
                    if (settings.numberOfMonths > 1) {
                        if (keyCode.RIGHT === which) {
                            $newDt = $datepicker.find('a[data-month="' + ++month + '"]:first');
                        } else if (keyCode.LEFT === which) {
                            $newDt = $datepicker.find('a[data-month="' + --month + '"]:last');
                        }

                        if ($newDt.length) {
                            e.preventDefault();

                            $newDt.focus();
                        }
                    } else {
                        date = new Date(++month + '/' + date + '/' + year);
                        if (keyCode.UP === which) {
                            e.preventDefault();
                            date = new Date(date.setTime(date.getTime() - (7 * 24 * 60 * 60 * 1000)));
                            $dateInput.datepicker('setDate', date);
                        } else if (keyCode.DOWN === which) {
                            e.preventDefault();
                            date = new Date(date.setTime(date.getTime() + (7 * 24 * 60 * 60 * 1000)));
                            $dateInput.datepicker('setDate', date);
                        }
                    }
                }
            }


            //if user is tabbing on dates
            if (keyCode.TAB === which) {
                e.preventDefault();

                if (e.shiftKey) {
                    $datepicker.find('.ui-datepicker-header a, .ui-datepicker-header select')
                        .not('.ui-state-disabled')
                        .last()
                        .focus();
                } else {
                    if (settings.showButtonPanel) {
                        $datepicker.find('.ui-datepicker-buttonpane button').filter(':visible').focus();
                    } else {
                        $datepicker.find('.ui-datepicker-next').focus();
                    }
                }
            }

        });

        $doc.on('click', 'a.ui-corner-all', function() {
            var $this = $(this);

            if (!$this.hasClass('.ui-state-disabled')) {
                if ($this.data('handler') === 'prev') {
                    module.clickedSelector = '.ui-datepicker-prev';
                } else {
                    module.clickedSelector = '.ui-datepicker-next';
                }
            }

        });
    }

    //defaults settings
    defaults = {
        showOn: 'button',
        buttonImage: '/images/calendar_orange_small.gif', // File (and file path) for the calendar image
        buttonImageOnly: false,
        buttonText: 'Calendar View',
        showButtonPanel: true,
        closeText: 'Close',
        dayNamesShort: dayNamesArr,
        onChangeMonthYear: populateAriaAttributes,
        onSelect: function() {
            //focus input date field
            setTimeout(function() {
                $dateInput.focus();
            }, 1);
        }
    };


    /**
     * Adds custom ui-datepicker widget
     *
     * @param {String|jQuery} dpContainer datepicker selector/element
     * @param {Object} options datepicker settings
     */
    module.addDatePicker = function addDatePicker(dpContainer, options) {
        //if dpContainer is jquery object
        if (dpContainer instanceof $) {
            $dateInput = dpContainer;
        } else {
            $dateInput = $(dpContainer);
        }

        if (!$dateInput.length) {
            return;
        }

        //merge defaults and given options
        settings = $.extend({}, defaults, options);


        //initialize datepicker
        $dateInput.datepicker(settings);

        // hold datepicker container once initialized
        $datepicker = $('#ui-datepicker-div');

        //attach event handlers
        attachEventHandlers();

        //set screenreader attributes
        $datepicker.attr({
            role: 'application',
            'aria-label': 'Calendar view date-picker'
        });

        //add wrapper around datepicker for llb styles
        $datepicker.wrap('<div class="hasDatePicker" />');
    };

    return module;
});