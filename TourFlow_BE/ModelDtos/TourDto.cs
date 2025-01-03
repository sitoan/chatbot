using System;
using System.Collections.Generic;

namespace TourFlowBE.Models;

public partial class TourDto
{
    public int Id { get; set; }

    public string? Destination { get; set; }

    public string? DepartureLocation { get; set; }

    public DateTime? StartDate { get; set; } 

    public DateTime? EndDate { get; set; }
    public TimeSpan? Duration {get; set;}

    public double? Price { get; set; }

    public int? AvailableSlots { get; set; } 
}
