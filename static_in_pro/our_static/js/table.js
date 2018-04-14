/**
 * Created by Arinze on 2/4/2017.
 */
$(document).ready(function() {
    $('.dataGrid, #example').DataTable({
    	"lengthMenu": [ 40, 60, 80, 100, 120, 140, 160 ],
        "pageLength": 50,
        "responsive": true,
        "ordering": false,
    });
     $('.dataGrid2,#example2').DataTable( {
        "ordering": false,
        "scrollY":        "200px",
        "scrollCollapse": true,
        "paging":         false,
        "destroy":        true,
    } );
    $('.dataGrid2,#example1').DataTable( {
        "ordering": false,
        "scrollY":        "200px",
        "scrollCollapse": true,
        "paging":         false,
        "destroy":        true,
    } );
     $('.dataGrid3,#example3').DataTable( {

        dom: 'Bfrtip',
         buttons:[
             'copy','csv','excel','pdf','print'
         ]
    } );
     $('.dataGrid4,#example4').DataTable( {
         "ordering": false,
         "bFilter": false,
         "bInfo": false,
         "paging": true,
         "dom": "lfrti",
        dom: 'Bfrtip',
         buttons:[
             'copy','csv','excel','pdf','print'
         ]
    } );

} );


