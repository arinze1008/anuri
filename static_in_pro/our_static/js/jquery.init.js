/**
 * Created by Arinze on 2/20/2017.
 */
var yl = yl || {};

if (yl.jQuery === undefined) {
    if (typeof django !== 'undefined')
        yl.jQuery = django.jQuery;

    else if (typeof $ !== 'undefined')
        yl.jQuery = $;
}