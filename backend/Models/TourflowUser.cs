using System;
using System.Collections.Generic;

namespace TourFlowBE.Models;

public partial class TourflowUser
{
    public int Id { get; set; }

    public string Email { get; set; } = null!;

    public string? TourflowUserName { get; set; }

    public bool? IsAdmin { get; set; }

    public string Jwt { get; set; } = null!;

    public string RefreshKey { get; set; } = null!;

    public string? AvatarUrl { get; set; }

    public virtual ICollection<TourOrder> TourOrders { get; set; } = new List<TourOrder>();

    public virtual ICollection<UserDataCollection> UserDataCollections { get; set; } = new List<UserDataCollection>();
}
