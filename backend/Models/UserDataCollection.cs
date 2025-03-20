using System;
using System.Collections.Generic;

namespace TourFlowBE.Models;

public partial class UserDataCollection
{
    public int Id { get; set; }

    public int? UserId { get; set; }

    public string? PhoneNumber { get; set; }

    public int? TourId { get; set; }

    public string? StarPos { get; set; }

    public string? EndPos { get; set; }

    public DateOnly? StartDate { get; set; }

    public string? Duration { get; set; }

    public double? Budget { get; set; }

    public int? AvailableSlot { get; set; }

    public virtual TourflowUser? User { get; set; }
}
