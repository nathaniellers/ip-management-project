import Swal from 'sweetalert2'

export const showError = async (message: string = 'Error!', text: string = "An error occurred. Please try again.") => {
  return await Swal.fire({
    icon: 'error',
    title: message,
    text,
    timer: 1500,
    showConfirmButton: false
  })
}
