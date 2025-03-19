using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace TourFlow_gitBE.ModelDtos
{
    public class TourOrderDto
    { 

    public int TourflowUserId { get; set; }

    public int TourBooked { get; set; }

    public int? Slots { get; set; }

    public double? TotalPrice { get; set; }

    }
}