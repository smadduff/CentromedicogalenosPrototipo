

    // Agregar método de validación para RUT chileno
    $.validator.addMethod("rutChileno", function(value, element) {
      // Eliminar puntos y guión del RUT
      value = value.replace(/[.-]/g, "");
  
      // Validar que el RUT tenga 8 o 9 dígitos
      if (value.length < 8 || value.length > 9) {
        return false;
      }
  
      // Validar que el último dígito sea un número o una 'K'
      var validChars = "0123456789K";
      var lastChar = value.charAt(value.length - 1).toUpperCase();
      if (validChars.indexOf(lastChar) == -1) {
        return false;
      }
  
      // Calcular el dígito verificador
      var rut = parseInt(value.slice(0, -1), 10);
      var factor = 2;
      var sum = 0;
      var digit;
      while (rut > 0) {
        digit = rut % 10;
        sum += digit * factor;
        rut = Math.floor(rut / 10);
        factor = factor === 7 ? 2 : factor + 1;
      }
      var dv = 11 - (sum % 11);
      dv = dv === 11 ? "0" : dv === 10 ? "K" : dv.toString();
  
      // Validar que el dígito verificador sea correcto
      return dv === lastChar;
    }, "Por favor ingrese un RUT válido."); 
  
    $.validator.setDefaults({
        messages: {
          required: 'Este campo es obligatorio',
        },
    });



$('#form').validate({
    rules: {
        'tipo_usuario': {
            required: true,
        },
        'rut': {
            required: true,
            rutChileno: true,
        },
        'nombres': {
            required: true,
            minlength: 3,
        },
        'apellidos': {
            required: true,
            minlength: 3,
        },
        'correo': {
            required: true,
            email: true,
        },
        'direccion': {
            required: true,
            minlength: 5,
        },
        'imagen': {
            required: true,
            extension: 'jpeg|jpg|png',
        },
    },
    messages: {
        'tipo_usuario': {
            required: 'El campo tipo de usuario es obligatorio',
        },
        'rut': {
            required: 'Debe ingresar su RUT',
            rutChileno: 'El formato del RUT no es válido',
          },
        'nombres': {
            required: 'El campo nombres es obligatorio',
            minlength: 'El campo nombres debe tener al menos 3 caracteres',
        },
        'apellidos': {
            required: 'El campo apellidos es obligatorio',
            minlength: 'El campo apellidos debe tener al menos 3 caracteres',
        },
        'correo': {
            required: 'El campo correo es obligatorio',
            email: 'Ingrese un correo electrónico válido',
        },
        'direccion': {
            required: 'El campo dirección es obligatorio',
            minlength: 'El campo dirección debe tener al menos 5 caracteres',
        },
        'imagen': {
            required: 'Seleccione una imagen',
            extension: 'El archivo debe tener una extensión válida (jpeg, jpg, png)',
        },
    },
    errorPlacement: function(error, element) {
        error.insertAfter(element); // Insert the error message after the element
        error.addClass('error-message'); // Add a class to the error message
    },
});
