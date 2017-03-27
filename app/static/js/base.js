String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

$('.logout').click(function(e){
    e.preventDefault();
    console.log('alala');
    document.location.href = '/auth/logout'
});


