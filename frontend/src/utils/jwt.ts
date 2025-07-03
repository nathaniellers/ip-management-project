import { UserPayload } from "../types/user"

export const decodeBase64User = (encoded: string): UserPayload => {
  try {
    const decoded = atob(encoded) // Decode base64 to string
    return JSON.parse(decoded) as UserPayload
  } catch (error) {
    console.error("Failed to decode user payload:", error)
    throw new Error("Invalid user payload")
  }
}
