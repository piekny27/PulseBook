document.getElementById("postBtn").onclick = function()
{
    path= '/profile';
    parameters=
    {
        x: document.getElementById("x").value,
        y: document.getElementById("y").value,
        height: document.getElementById("height").value,
        width: document.getElementById("width").value,
    };

    var form = $('<form></form>');

    form.attr("method", "post");
    form.attr("action", path);

    $.each(parameters, function(key, value) {
        var field = $('<input></input>');

        field.attr("type", "hidden");
        field.attr("name", key);
        field.attr("value", value);

        form.append(field);
    });

    $(document.body).append(form);
    form.submit();
};

$(document).ready(function(){
    $("#image-crop").modal('show');
});