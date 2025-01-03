using TourFlow_gitBE.Services;
using Microsoft.AspNetCore.Mvc;
using TourFlowBE.Models;
using TourFlowBE.ModelDtos;
using Microsoft.AspNetCore.Authorization;
using Microsoft.EntityFrameworkCore;

namespace TourFlow_gitBE.Contollers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AuthController : ControllerBase
    { 
        private readonly TourFlowContext _dbContext;
        private readonly GoogleTokenService _googleTokenService;
        private readonly ITokenGenerating _tokenGenerating;
        public AuthController(TourFlowContext dbContext
                    , ITokenGenerating tokenGenerating
                    , GoogleTokenService googleTokenService)
        {
            _dbContext = dbContext;
            _googleTokenService = googleTokenService;
            _tokenGenerating = tokenGenerating;
        }

        [HttpGet]
public async Task<IActionResult> Get()
{
    var result = await (from user in _dbContext.TourflowUsers
                        join order in _dbContext.TourOrders on user.Id equals order.TourflowUserId
                        join tour in _dbContext.Tours on order.TourBooked equals tour.Id
                        join city in _dbContext.CityDestinations on tour.CityDestinationId equals city.Id
                        where user.IsAdmin == false
                        select new 
                        {
                            userId = user.Id,
                            userName = user.TourflowUserName,
                            userEmail = user.Email,
                            avatar = user.AvatarUrl,
                            bookDate = order.BookDate,
                            cityDestination = city.City
                        })
                        .GroupBy(x => new {x.userId, x.userName, x.userEmail, x.avatar })
                        .Select(g => new
                        {
                            g.Key.userId,   
                            g.Key.userName,
                            g.Key.userEmail,
                            g.Key.avatar,
                            tours = g.Select(x => new 
                            {
                                cityDestination = x.cityDestination,
                                bookDate = x.bookDate
                            }).ToList()
                        })
                        .ToListAsync();

    return Ok(result);
}

        
        [AllowAnonymous]
        [HttpPost("google-signin")]
        public async Task<IActionResult> GoogleSignIn([FromBody] GoogleSignInRequest request)
        {  
            try 
            { 
                var payload = await _googleTokenService.ValidateGoogleToken(request.IdToken); 
                var customer = new GoogleSignInDto{ 
                    Email = payload.Email,
                    Name = payload.GivenName + payload.FamilyName,
                    AvaUrl = payload.Picture,
                };  
                var jwt = _tokenGenerating.GenerateJWT(customer); 
 
                var currentCustomer = _dbContext.TourflowUsers
                        .FirstOrDefault(c=>c.Email == payload.Email);
                // resgister 
                if (currentCustomer == null)
                {
                    Console.WriteLine("go here");
                    var refreshToken = _tokenGenerating.GenerateRefreshToken(payload.Name);
                    var newCustomer = new TourflowUser{
                        Email = payload.Email,
                        TourflowUserName = payload.Name,
                        Jwt = jwt,
                        RefreshKey = refreshToken,
                        AvatarUrl = payload.Picture,
                    };
                    _dbContext.TourflowUsers.Add(newCustomer);
                    Console.WriteLine("New customer: "+ newCustomer.Email);
                    await _dbContext.SaveChangesAsync();
                    return Ok(new { 
                        id = newCustomer.Id,
                        jwt,
                        Name = payload.Name,
                        avaUrl = payload.Picture,
                        refreshKey = refreshToken
                    });
                } else {
                    Console.WriteLine("Role: " + currentCustomer.IsAdmin);
                   return Ok(new { 
                    id = currentCustomer.Id,
                    jwt,
                    refreshKey = currentCustomer.RefreshKey,
                    Name = currentCustomer.TourflowUserName,
                    avaUrl = currentCustomer.AvatarUrl,
                    role = currentCustomer.IsAdmin
                   });
                }
            } catch (Exception e) {
                return BadRequest(e.Message);
            }
        
        }
    }
    public class GoogleSignInRequest
    {
        public string IdToken { get; set; }
    }


}