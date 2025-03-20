using System;
using System.Collections.Generic;

namespace TourFlowBE.Models;

public partial class TourOrder
{
    public int Id { get; set; }

    public DateTime? BookDate { get; set; }

    public int TourflowUserId { get; set; }

    public int TourBooked { get; set; }

    public int? Slots { get; set; }

    public double? TotalPrice { get; set; }

    public bool? Paid { get; set; }

    public virtual Tour TourBookedNavigation { get; set; } = null!;

    public virtual TourflowUser TourflowUser { get; set; } = null!;
}
