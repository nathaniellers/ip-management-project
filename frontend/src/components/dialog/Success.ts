import Swal from 'sweetalert2'

export const showSuccess = async (message: string = 'Update successful!', text: string = "") => {
  return await Swal.fire({
    icon: 'success',
    title: message,
    text,
    timer: 1500,
    showConfirmButton: false
  })
}
