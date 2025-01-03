using Google.Apis.Auth;
namespace TourFlow_gitBE.Services
{
    public class GoogleTokenService
    {
        public async Task<GoogleJsonWebSignature.Payload> ValidateGoogleToken(string idToken)
        {
            try
            {
                if (string.IsNullOrEmpty(idToken))
                {
                    throw new ArgumentNullException(nameof(idToken), "ID token cannot be null or empty.");
                }
                // Giải mã và xác thực token ID 
                var payload = await GoogleJsonWebSignature.ValidateAsync(idToken);
                return payload;
            }
            catch (InvalidJwtException ex)
            {
                // Token không hợp lệ
                throw new Exception("Invalid Google ID token", ex);
            }
        }
    }
}