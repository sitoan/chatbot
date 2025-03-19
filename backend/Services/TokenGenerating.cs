using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;
using TourFlowBE.Models;
using TourFlowBE.ModelDtos; 
namespace TourFlow_gitBE.Services
{
    public interface ITokenGenerating 
    {
       public string GenerateJWT(GoogleSignInDto customer);
        public string GenerateRefreshToken(string customerName);
    }
    public class TokenGenerating : ITokenGenerating
    {
        private readonly IConfiguration _config;
        private readonly TourFlowContext _dbContext;
        public TokenGenerating(IConfiguration config, TourFlowContext dbContext)
        {
            _config = config;
            _dbContext = dbContext;
        }
        public string GenerateJWT(GoogleSignInDto customer)
        { 
            var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(this._config["Jwt:Key"]));
            var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);
            
            

            var claims = new List<Claim>
            {
                new Claim(ClaimTypes.NameIdentifier, customer.Name), 
                new Claim(ClaimTypes.Email, customer.Email),
                // new Claim(ClaimTypes.Role, customer.Role.ToString()),
            }; 
            var existedUser = _dbContext.TourflowUsers
                        .FirstOrDefault(c=>c.Email == customer.Email);
            if (existedUser != null ){
                claims.Add(new Claim(ClaimTypes.Role, existedUser.IsAdmin.ToString()));
            }
 
            var token = new JwtSecurityToken(
                _config["Jwt:Issuer"],
                _config["Jwt:Audience"],
                claims,
                expires: DateTime.UtcNow.AddHours(20),
                signingCredentials: credentials
            );
            
            Console.WriteLine($"CREATE TIME: {DateTime.UtcNow}");
            Console.WriteLine($"EXPIRATION WHEN CREATE: {DateTime.UtcNow.AddHours(2)}");
            return new JwtSecurityTokenHandler().WriteToken(token);
        }

        public string GenerateRefreshToken(string customerName)
        {
             return Guid.NewGuid().ToString();
           
        }
    }
}