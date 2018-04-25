// $(document).ready(function() {
//     // $('#dataTable').DataTable();

//     // $.fn.dataTableExt.afnFiltering.push(function(oSettings, aData, iDataIndex) {
//     // var checked = $('#checkbox').is(':checked');

//     // if (checked && aData[4] > 3) {
//     //     return true;
//     // }
//     // if (!checked && aData[4] <= 5) {
//     //     return true;
//     // }
//     // return false;
//     // });
//     // var oTable = $('#dataTable').dataTable();
//     // $('#checkbox').on("click", function(e) {
//     //     console.log('click');
//     //     oTable.fnDraw();
//     // });
//     $('#dataTable').DataTable().column(col).search(regex, true, true).draw();
// } );
// // Code goes here

// Code goes here

$(function() {
  otable = $('#dataTable').dataTable();
})

function filterme() {
  //build a regex filter string with an or(|) condition
  // var stars = $('input:checkbox[name="free"]:checked').map(function() {
  // 	console.log("ok");
  //   return '^' + this.value + '\$';
  // }).get().join('|');
  // //filter in column 0, with an regex, no smart filtering, no inputbox,not case sensitive
  // otable.fnFilter(stars, 4, true, false, false, false);

	var cate = $('input:checkbox[name="cate"]:checked').map(function(){
		return '^'+this.value+'\$';
	}).get().join('|');
	//now filter in column 4, with no regex, no smart filtering, no inputbox,not case sensitive
	otable.fnFilter(cate, 2, true, true, false, false);

	var star = $('input:checkbox[name="stars"]:checked').map(function(){
		return '^'+this.value+'\$';
	}).get().join('|');
	//now filter in column 4, with no regex, no smart filtering, no inputbox,not case sensitive
	otable.fnFilter(star, 4, true, false, false, false);

	var city = $('input:checkbox[name="city"]:checked').map(function(){
		return '^'+this.value+'\$';
	}).get().join('|');
	//now filter in column 3, with no regex, no smart filtering, no inputbox,not case sensitive
	otable.fnFilter(city, 3, true, false, false, false);
}